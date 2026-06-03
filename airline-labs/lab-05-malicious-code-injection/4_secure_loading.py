#!/usr/bin/env python3
"""
Lab 05: Secure Model Loading - Detect Backdoors

Demonstrates security checks that detect the backdoored model
before it's loaded into production.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import sys
import numpy as np
import joblib
import inspect
import os
from pathlib import Path

# Ensure BackdooredModel class is importable for pickle deserialization
sys.path.insert(0, str(Path(__file__).parent))
from backdoor_model import BackdooredModel  # noqa: F401

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Dangerous patterns to scan for in model code
DANGEROUS_PATTERNS = [
    'socket', 'requests.post', 'urllib', 'http.client',
    'subprocess', 'os.system', 'eval(', 'exec(',
    'open(', 'write(', 'exfiltrat', 'send_to',
    '_exfil', 'backdoor', 'hidden_', 'covert_',
]

# Expected model classes for baggage screening
ALLOWED_MODEL_CLASSES = [
    'RandomForestClassifier',
    'GradientBoostingClassifier',
    'MLPClassifier',
    'SVC',
]


def scan_model_code(model):
    """Inspect model source code for suspicious patterns."""
    findings = []

    # Get the class name
    class_name = type(model).__name__

    # Check if it's a known/approved model class
    if class_name not in ALLOWED_MODEL_CLASSES:
        findings.append({
            'severity': 'HIGH',
            'finding': f'Unknown model class: {class_name}',
            'detail': f'Expected one of: {ALLOWED_MODEL_CLASSES}'
        })

    # Try to inspect source code
    try:
        source = inspect.getsource(type(model))
        for pattern in DANGEROUS_PATTERNS:
            if pattern in source.lower():
                findings.append({
                    'severity': 'CRITICAL',
                    'finding': f'Dangerous pattern found: "{pattern}"',
                    'detail': 'Model code contains potentially malicious operations'
                })
    except (TypeError, OSError):
        # Built-in sklearn models won't have inspectable source in some cases
        pass

    # Check for unexpected attributes
    suspicious_attrs = []
    for attr in dir(model):
        if attr.startswith('_') and not attr.startswith('__'):
            if any(p in attr.lower() for p in ['exfil', 'send', 'hidden', 'backdoor', 'covert']):
                suspicious_attrs.append(attr)

    if suspicious_attrs:
        findings.append({
            'severity': 'CRITICAL',
            'finding': f'Suspicious attributes: {suspicious_attrs}',
            'detail': 'Model has hidden methods suggesting malicious behavior'
        })

    # Check for wrapped/proxy models
    if hasattr(model, 'model') and hasattr(model, 'predict'):
        findings.append({
            'severity': 'HIGH',
            'finding': 'Model appears to be a wrapper/proxy',
            'detail': 'Legitimate models do not wrap other models with custom predict()'
        })

    return findings


def verify_model_behavior(model, n_tests=100):
    """Test model for unexpected side effects."""
    findings = []

    # Generate test data
    np.random.seed(42)
    X_test = np.random.uniform(0, 1, (n_tests, 8))

    # Check if model creates files during prediction
    lab_dir = Path(__file__).parent
    files_before = set(lab_dir.rglob('*'))

    try:
        predictions = model.predict(X_test)
    except Exception as e:
        findings.append({
            'severity': 'HIGH',
            'finding': f'Model prediction raised unexpected error: {type(e).__name__}',
            'detail': str(e)
        })
        return findings

    files_after = set(lab_dir.rglob('*'))
    new_files = files_after - files_before

    if new_files:
        findings.append({
            'severity': 'CRITICAL',
            'finding': f'Model created {len(new_files)} files during prediction!',
            'detail': f'New files: {[str(f.name) for f in new_files]}'
        })

    # Check prediction output validity
    unique_preds = set(predictions)
    if any(p < 0 or p > 4 for p in unique_preds):
        findings.append({
            'severity': 'MEDIUM',
            'finding': 'Model produces out-of-range predictions',
            'detail': f'Expected 0-4, got: {unique_preds}'
        })

    return findings


def secure_loading():
    """Run security checks on the model before allowing production use."""
    print(f"""
{BOLD}{GREEN}
{'='*60}
  LAB 05: Secure Model Loading - Backdoor Detection
{'='*60}
{RESET}
  {CYAN}Running pre-deployment security checks on the baggage
  screening model before allowing it into production.{RESET}
""")

    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "baggage_screening_model.joblib"

    if not model_path.exists():
        print(f"  {RED}[FAIL] Model not found. Run previous steps first.{RESET}")
        return

    print(f"  {BOLD}Security Scan Results:{RESET}")
    print(f"  {'='*50}")

    # Load model for inspection
    print(f"\n  {CYAN}[1/4] Loading model for inspection...{RESET}")
    model_data = joblib.load(model_path)
    model = model_data['model']
    print(f"    Model class: {type(model).__name__}")
    print(f"    Version: {model_data['version']}")

    all_findings = []

    # Check 1: Code inspection
    print(f"\n  {CYAN}[2/4] Scanning model code for suspicious patterns...{RESET}")
    code_findings = scan_model_code(model)
    all_findings.extend(code_findings)

    for finding in code_findings:
        sev = finding['severity']
        color = RED if sev == 'CRITICAL' else YELLOW if sev == 'HIGH' else BLUE
        print(f"    {color}[{sev}]{RESET} {finding['finding']}")
        print(f"           {finding['detail']}")

    if not code_findings:
        print(f"    {GREEN}[OK] No suspicious code patterns found.{RESET}")

    # Check 2: Behavioral analysis
    print(f"\n  {CYAN}[3/4] Running behavioral analysis (sandboxed inference)...{RESET}")
    behavior_findings = verify_model_behavior(model)
    all_findings.extend(behavior_findings)

    for finding in behavior_findings:
        sev = finding['severity']
        color = RED if sev == 'CRITICAL' else YELLOW if sev == 'HIGH' else BLUE
        print(f"    {color}[{sev}]{RESET} {finding['finding']}")
        print(f"           {finding['detail']}")

    if not behavior_findings:
        print(f"    {GREEN}[OK] No suspicious behavior detected.{RESET}")

    # Check 3: Model integrity
    print(f"\n  {CYAN}[4/4] Checking model integrity...{RESET}")
    expected_class = 'RandomForestClassifier'
    actual_class = type(model).__name__

    if actual_class != expected_class:
        print(f"    {RED}[CRITICAL] Expected {expected_class}, got {actual_class}{RESET}")
    else:
        print(f"    {GREEN}[OK] Model class matches expected: {actual_class}{RESET}")

    # Final verdict
    critical_count = sum(1 for f in all_findings if f['severity'] == 'CRITICAL')
    high_count = sum(1 for f in all_findings if f['severity'] == 'HIGH')

    print(f"\n  {'='*50}")
    print(f"  {BOLD}SECURITY VERDICT:{RESET}")
    print(f"  {'='*50}")

    if critical_count > 0:
        print(f"""
  {RED}{BOLD}  BLOCKED - MODEL REJECTED{RESET}

  {RED}  Critical findings: {critical_count}{RESET}
  {YELLOW}  High findings: {high_count}{RESET}

  {RED}  This model contains malicious code and MUST NOT be
  deployed to production. The model has been quarantined.{RESET}

  {BOLD}  Recommended Actions:{RESET}
  1. Investigate model supply chain
  2. Check model storage access logs
  3. Verify model signing certificates
  4. Retrain from trusted source data
  5. Report to security team
""")
    elif high_count > 0:
        print(f"""
  {YELLOW}{BOLD}  WARNING - MANUAL REVIEW REQUIRED{RESET}

  {YELLOW}  High findings: {high_count}{RESET}

  {YELLOW}  Model has suspicious characteristics. Manual review
  by security team required before deployment.{RESET}
""")
    else:
        print(f"""
  {GREEN}{BOLD}  APPROVED - MODEL CLEARED FOR DEPLOYMENT{RESET}

  {GREEN}  No security issues found. Model may be deployed.{RESET}
""")


if __name__ == "__main__":
    secure_loading()
