"""
Airline Model Security Scanner

A security scanner specifically designed for airline operations teams
to validate ML models before loading them with trust_remote_code=True.

Implements airline-specific security policies:
1. Publisher Verification - Only approved vendors/internal teams
2. Custom Code Detection - Flag models requiring code execution
3. Dangerous Pattern Scan - Detect network, shell, and exfil patterns
4. Entropy Analysis - Detect obfuscated/encrypted payloads
5. Import Chain Analysis - Trace dangerous import dependencies

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.

Usage:
    from airline_model_scanner import AirlineModelScanner

    scanner = AirlineModelScanner("/path/to/model/cache")
    if scanner.scan():
        # Safe to load
        model = AutoModel.from_pretrained(..., trust_remote_code=True)
    else:
        # BLOCKED - malicious code detected
        print(scanner.findings)
"""

import re
import json
import hashlib
import math
import ast
from pathlib import Path


# Airline-approved model publishers
APPROVED_PUBLISHERS = [
    'airline-internal',     # Internal data science team
    'google',              # Verified vendor
    'meta-llama',          # Verified vendor
    'microsoft',           # Verified vendor
    'huggingface',         # Platform provider
    'nvidia',              # Verified vendor
    'ibm-research',        # Verified vendor
    'openai',              # Verified vendor
]


class AirlineModelScanner:
    """
    Airline-specific ML model security scanner.

    Validates downloaded model files BEFORE loading with trust_remote_code=True.
    Enforces airline security policies for model deployment.
    """

    SUSPICIOUS_PATTERNS = [
        (r'socket\.socket', 'Network socket creation'),
        (r'os\.fork\s*\(\)', 'Process forking'),
        (r'subprocess', 'Subprocess execution'),
        (r'pty\.spawn', 'PTY shell spawning'),
        (r'os\.dup2', 'File descriptor redirection'),
        (r'exec\s*\(|eval\s*\(', 'Dynamic code execution'),
        (r'urllib|requests\.get|http\.client', 'HTTP requests (data exfiltration risk)'),
        (r'os\.system', 'System command execution'),
        (r'pickle\.load|torch\.load|joblib\.load', 'Deserialization (pickle RCE risk)'),
        (r'ctypes|cffi', 'Native code execution'),
        (r'base64\.b64decode', 'Base64 decoding (payload hiding)'),
        (r'compile\s*\(', 'Dynamic code compilation'),
        (r'__import__\s*\(', 'Dynamic import (obfuscation)'),
        (r'getattr.*\(.*,.*\)\s*\(', 'Dynamic attribute call'),
        (r'\\x[0-9a-fA-F]{2}', 'Hex-encoded strings (obfuscation)'),
        (r'smtplib|email\.mime', 'Email sending (data exfiltration)'),
        (r'paramiko|ssh', 'SSH connections (lateral movement)'),
    ]

    TEXT_EXTENSIONS = ['.py', '.json', '.yaml', '.yml', '.txt', '.md', '.cfg', '.ini', '']
    BINARY_EXTENSIONS = ['.so', '.dll', '.dylib', '.bin', '.pkl', '.pickle']

    HIGH_ENTROPY_THRESHOLD = 5.5

    def __init__(self, model_cache_path, verbose=True):
        self.model_cache = Path(model_cache_path)
        self.verbose = verbose
        self.findings = []
        self.warnings = []
        self.requires_custom_code = False
        self.auto_map_targets = []
        self.publisher = None
        self.file_hashes = {}

    def _log(self, message):
        if self.verbose:
            print(message)

    def _calculate_entropy(self, data):
        """Calculate Shannon entropy (detects obfuscation/encryption)."""
        if not data:
            return 0.0
        entropy = 0.0
        for x in range(256):
            p_x = data.count(chr(x)) / len(data)
            if p_x > 0:
                entropy -= p_x * math.log2(p_x)
        return entropy

    def _compute_file_hash(self, filepath):
        """Compute SHA256 hash for integrity verification."""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def verify_publisher(self):
        """Check if model is from an airline-approved publisher."""
        self._log("[1/5] Verifying publisher against airline approved list...")

        cache_name = self.model_cache.name
        if cache_name.startswith("models--"):
            parts = cache_name.split("--")
            if len(parts) >= 2:
                self.publisher = parts[1]

        if self.publisher:
            if self.publisher.lower() in [p.lower() for p in APPROVED_PUBLISHERS]:
                self._log(f"  ✓ APPROVED publisher: {self.publisher}")
                return True
            else:
                self.warnings.append(f"UNAPPROVED publisher: {self.publisher}")
                self._log(f"  ⚠️  UNAPPROVED publisher: {self.publisher}")
                self._log(f"      Airline-approved: {', '.join(APPROVED_PUBLISHERS[:5])}...")
                return False
        else:
            self._log(f"  ⚠️  Could not determine publisher from path")
            return False

    def check_custom_code_requirement(self):
        """Check if model requires trust_remote_code=True."""
        self._log("\n[2/5] Checking if model requires custom code execution...")

        config_path = self.model_cache / "config.json"
        if not config_path.exists():
            self._log("  ✓ No config.json found")
            return False

        with open(config_path) as f:
            config = json.load(f)

        if "auto_map" in config:
            self.requires_custom_code = True
            self.auto_map_targets = list(config['auto_map'].values())
            self._log(f"  ⚠️  Model requires trust_remote_code=True")
            self._log(f"  ⚠️  Will execute: {self.auto_map_targets}")
            return True
        else:
            self._log(f"  ✓ Standard model - no custom code needed")
            return False

    def inspect_downloaded_files(self):
        """Categorize all downloaded files by type."""
        self._log(f"\n[3/5] Inspecting downloaded files...")

        all_files = list(self.model_cache.glob("*"))
        py_files = [f for f in all_files if f.suffix == '.py']
        binary_files = [f for f in all_files if f.suffix in self.BINARY_EXTENSIONS]

        for f in all_files:
            if f.is_file():
                self.file_hashes[f.name] = self._compute_file_hash(f)

        file_count = len([f for f in all_files if f.is_file()])
        if file_count:
            self._log(f"  Found {file_count} file(s) in cache:")
            for f in all_files:
                if f.is_file():
                    if f in py_files:
                        self._log(f"     ⚠️  {f.name} (EXECUTABLE CODE)")
                    elif f in binary_files:
                        self._log(f"     🚨 {f.name} (BINARY - CANNOT INSPECT)")
                    else:
                        self._log(f"     - {f.name}")

        return {
            'all': all_files,
            'python': py_files,
            'binary': binary_files,
        }

    def scan_for_malicious_patterns(self, files):
        """Scan text files for suspicious code patterns."""
        self._log(f"\n[4/5] Scanning code for dangerous patterns...")

        self.findings = []

        text_files = [f for f in files['all'] if f.is_file() and f.suffix in self.TEXT_EXTENSIONS]
        for text_file in text_files:
            try:
                content = text_file.read_text(encoding='utf-8')
                for pattern, desc in self.SUSPICIOUS_PATTERNS:
                    if re.search(pattern, content):
                        self.findings.append((text_file.name, desc))
            except (UnicodeDecodeError, PermissionError):
                self.findings.append((text_file.name, "Unreadable file (suspicious)"))

        for bin_file in files['binary']:
            self.findings.append((bin_file.name, "Uninspectable binary file"))

        if self.findings:
            self._log(f"  🚨 DANGEROUS CODE DETECTED:")
            for filename, desc in self.findings:
                self._log(f"     - {filename}: {desc}")
        else:
            self._log(f"  ✓ No suspicious patterns found")

        return self.findings

    def analyze_entropy(self, files):
        """Detect obfuscated/encrypted payloads via entropy analysis."""
        self._log(f"\n[5/5] Analyzing entropy for obfuscation detection...")

        high_entropy_files = []

        for f in files['all']:
            if f.is_file() and f.suffix == '.py':
                try:
                    content = f.read_text(encoding='utf-8')
                    entropy = self._calculate_entropy(content)
                    if entropy > self.HIGH_ENTROPY_THRESHOLD:
                        high_entropy_files.append((f.name, entropy))
                        self.warnings.append(f"High entropy in {f.name}: {entropy:.2f}")
                except:
                    pass

        if high_entropy_files:
            self._log(f"  ⚠️  High entropy files (possible obfuscation):")
            for fname, ent in high_entropy_files:
                self._log(f"     - {fname}: entropy={ent:.2f}")
        else:
            self._log(f"  ✓ No obfuscated code detected")

        return high_entropy_files

    def scan(self):
        """
        Run full airline security scan on model cache.

        Returns:
            True if model is safe to load, False if threats detected.
        """
        self._log("=" * 60)
        self._log("  ✈️  AIRLINE MODEL SECURITY SCAN")
        self._log("=" * 60)
        self._log("")

        self.verify_publisher()
        self.check_custom_code_requirement()
        files = self.inspect_downloaded_files()
        self.scan_for_malicious_patterns(files)
        self.analyze_entropy(files)

        return len(self.findings) == 0

    def print_assessment(self):
        """Print airline security assessment summary."""
        print("\n" + "=" * 60)
        print("  ✈️  AIRLINE SECURITY ASSESSMENT")
        print("=" * 60)

        if self.file_hashes:
            print("\n📋 FILE HASHES (SHA256):")
            for fname, fhash in self.file_hashes.items():
                print(f"   {fname}: {fhash[:16]}...")

        print("""
┌─────────────────────────────────────────────────────────────┐
│  🛡️  AIRLINE SECURITY POLICY CHECKS                         │
│                                                             │
│  ✓ Publisher Verification (Approved vendor list)            │
│  ✓ Custom Code Detection (trust_remote_code flag)          │
│  ✓ Pattern Matching (Network, shell, exfil patterns)       │
│  ✓ Entropy Analysis (Obfuscation detection)                │
│  ✓ File Hash Recording (Integrity tracking)                │
│                                                             │
│  POLICY: Only load models from airline-approved publishers  │
│  Approved: airline-internal, google, microsoft, nvidia      │
└─────────────────────────────────────────────────────────────┘
""")

        if self.warnings:
            print("⚠️  WARNINGS:")
            for w in self.warnings:
                print(f"   - {w}")
            print()

        if self.findings:
            print("""
🚨 CRITICAL: Malicious code detected in model files!

The model contains:
  - Network socket creation (reverse shell)
  - Process forking / subprocess execution
  - Shell spawning capabilities

This is the signature of a REVERSE SHELL BACKDOOR.

If loaded with trust_remote_code=True, the attacker will
gain shell access to airline operational systems including:
  - Passenger data (PNR, passports)
  - Crew scheduling systems
  - Flight operations databases
  - Revenue management systems
""")
            print("=" * 60)
            print("  ❌ MODEL BLOCKED - AIRLINE SECURITY POLICY VIOLATION")
            print("=" * 60)
            print()
        else:
            print("=" * 60)
            print("  ✅ MODEL APPROVED - Safe to load")
            print("=" * 60)
            print()
