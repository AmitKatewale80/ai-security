#!/usr/bin/env python3
"""
Step 4: Defense — Multi-Layer Code Review

Combines AI review + SAST (Static Analysis) + semantic checks
to catch what AI alone misses.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import re
import base64
import time

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

PR_CODE = [
    {
        'title': 'PR #1: Refactor user lookup',
        'code': '''def get_user_profile(db_conn, user_identifier):
    lookup_template = "SELECT * FROM users WHERE id = "
    optimized_query = lookup_template + str(user_identifier)
    cursor = db_conn.cursor()
    cursor.execute(optimized_query)
    return cursor.fetchone()''',
    },
    {
        'title': 'PR #2: Add config loader',
        'code': '''import base64
_SVC_AUTH = base64.b64decode(b'YWRtaW46UEBzc3cwcmQxMjM=').decode()
def get_service_headers():
    return {"Authorization": f"Basic {_SVC_AUTH}"}''',
    },
    {
        'title': 'PR #3: Add health check',
        'code': '''@app.route('/api/internal/health_extended')
def extended_health():
    import psutil
    return jsonify({
        "env_vars": dict(os.environ),
        "db_url": app.config.get('SQLALCHEMY_DATABASE_URI'),
    })''',
    },
    {
        'title': 'PR #4: File converter',
        'code': '''def convert_document(input_path, output_format):
    converter_args = ["libreoffice", "--convert-to", output_format, input_path]
    result = subprocess.run(" ".join(converter_args), shell=True, capture_output=True)
    return result.stdout''',
    },
]


def sast_scan(code):
    """Static Analysis Security Testing — deeper than pattern matching."""
    findings = []

    # Check 1: String concatenation with SQL keywords
    if re.search(r'SELECT.*FROM', code) and ('+' in code or 'str(' in code):
        findings.append(('HIGH', 'SQL Injection: String concatenation with query'))

    # Check 2: Base64 decoded values used in auth
    if 'base64' in code and ('Auth' in code or 'password' in code.lower()):
        findings.append(('HIGH', 'Hardcoded credential: base64 encoded secret'))

    # Check 3: os.environ exposed in response
    if 'os.environ' in code and ('jsonify' in code or 'return' in code):
        findings.append(('CRITICAL', 'Information disclosure: env vars in response'))

    # Check 4: Unauthenticated routes
    if '@app.route' in code and 'login_required' not in code and '@requires_auth' not in code:
        if 'internal' in code or 'admin' in code:
            findings.append(('HIGH', 'Missing auth on sensitive endpoint'))

    # Check 5: shell=True with user input
    if 'shell=True' in code and ('join(' in code or 'format' in code):
        findings.append(('CRITICAL', 'Command injection: shell=True with dynamic input'))

    # Check 6: subprocess without input validation
    if 'subprocess' in code and 'shell=True' in code:
        findings.append(('HIGH', 'Unsafe subprocess: shell=True should be avoided'))

    return findings


def semantic_check(code):
    """Semantic analysis — understands WHAT the code does, not just patterns."""
    findings = []

    # Check: Does a DB execute use parameterized queries?
    if '.execute(' in code and '?' not in code and '%s' not in code:
        if 'SELECT' in code or 'INSERT' in code or 'UPDATE' in code:
            findings.append(('MEDIUM', 'Non-parameterized query detected'))

    # Check: Does any function parameter flow into a dangerous sink?
    if 'def ' in code:
        # Extract function params
        params = re.findall(r'def \w+\([^)]*\)', code)
        if params and ('execute' in code or 'system' in code or 'shell' in code):
            findings.append(('MEDIUM', 'User-controlled input may reach dangerous function'))

    return findings


def run_multi_layer_review():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  DEFENSE: Multi-Layer Code Review{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}Pipeline: AI Review → SAST Scan → Semantic Analysis{RESET}")
    print(f"  {CYAN}ALL layers must pass for approval.{RESET}\n")

    total_caught = 0

    for pr in PR_CODE:
        print(f"  {BOLD}{'─'*55}{RESET}")
        print(f"  {BOLD}{pr['title']}{RESET}")
        print(f"  {BOLD}{'─'*55}{RESET}")

        # Layer 1: AI (same as before — may miss)
        time.sleep(0.3)
        print(f"\n    {CYAN}Layer 1 — AI Pattern Review:{RESET}")
        print(f"      {GREEN}✅ No obvious patterns found{RESET}")

        # Layer 2: SAST
        sast_findings = sast_scan(pr['code'])
        print(f"\n    {CYAN}Layer 2 — SAST (Static Analysis):{RESET}")
        if sast_findings:
            for severity, msg in sast_findings:
                color = RED if severity in ('HIGH', 'CRITICAL') else YELLOW
                print(f"      {color}[{severity}] {msg}{RESET}")
            total_caught += 1
        else:
            print(f"      {GREEN}✅ No issues{RESET}")

        # Layer 3: Semantic
        sem_findings = semantic_check(pr['code'])
        print(f"\n    {CYAN}Layer 3 — Semantic Analysis:{RESET}")
        if sem_findings:
            for severity, msg in sem_findings:
                print(f"      {YELLOW}[{severity}] {msg}{RESET}")
        else:
            print(f"      {GREEN}✅ No issues{RESET}")

        # Decision
        all_findings = sast_findings + sem_findings
        if all_findings:
            max_sev = 'CRITICAL' if any(s == 'CRITICAL' for s, _ in all_findings) else 'HIGH'
            print(f"\n    {RED}Final Decision: ❌ REJECTED ({max_sev}){RESET}")
        else:
            print(f"\n    {GREEN}Final Decision: ✅ APPROVED{RESET}")
        print()

    # Summary
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{GREEN}  MULTI-LAYER REVIEW RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    AI alone caught:          0/4 vulnerabilities")
    print(f"    AI + SAST + Semantic:      {GREEN}{total_caught}/4 vulnerabilities{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n  {BOLD}Defense Layers:{RESET}")
    print(f"    1. AI Pattern Review      — Fast, catches obvious issues")
    print(f"    2. SAST (Bandit/Semgrep)  — Catches obfuscated patterns")
    print(f"    3. Semantic Analysis      — Understands data flow")
    print(f"    4. Human Review (critical) — Final gate for HIGH/CRITICAL")

    print(f"\n  {GREEN}✅ No vulnerable code ships to production.{RESET}\n")


if __name__ == "__main__":
    run_multi_layer_review()
