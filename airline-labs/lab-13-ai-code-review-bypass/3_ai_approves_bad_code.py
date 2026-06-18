#!/usr/bin/env python3
"""
Step 3: AI Reviewer Approves Vulnerable Code

The AI code reviewer checks all 4 PRs and approves them —
missing every hidden vulnerability.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import re
import time

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# AI's detection patterns (same as the real reviewer would use)
DETECTION_PATTERNS = {
    'sql_injection': [r'execute\(f["\']', r'f["\']SELECT', r'format\(.*sql', r'%s.*execute'],
    'hardcoded_secrets': [r'password\s*=\s*["\']', r'api_key\s*=\s*["\']', r'secret\s*=\s*["\']'],
    'command_injection': [r'os\.system\(', r'subprocess\.call\(f', r'\beval\(', r'\bexec\('],
    'xss': [r'innerHTML\s*=', r'document\.write\('],
}

# The obfuscated code (same as step 2)
PR_CODE = [
    {
        'title': 'PR #1: Refactor user lookup',
        'code': '''def get_user_profile(db_conn, user_identifier):
    lookup_template = "SELECT * FROM users WHERE id = "
    optimized_query = lookup_template + str(user_identifier)
    cursor = db_conn.cursor()
    cursor.execute(optimized_query)
    return cursor.fetchone()''',
        'actual_vuln': 'SQL Injection',
    },
    {
        'title': 'PR #2: Add config loader',
        'code': '''import base64
_SVC_AUTH = base64.b64decode(b'YWRtaW46UEBzc3cwcmQxMjM=').decode()
def get_service_headers():
    return {"Authorization": f"Basic {_SVC_AUTH}"}''',
        'actual_vuln': 'Hardcoded Credentials (base64 encoded)',
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
        'actual_vuln': 'Unauthenticated endpoint exposes secrets',
    },
    {
        'title': 'PR #4: File converter',
        'code': '''def convert_document(input_path, output_format):
    converter_args = ["libreoffice", "--convert-to", output_format, input_path]
    result = subprocess.run(" ".join(converter_args), shell=True, capture_output=True)
    return result.stdout''',
        'actual_vuln': 'Command Injection via shell=True',
    },
]


def ai_review(code):
    """Simulate AI code review — pattern matching."""
    findings = []
    for vuln_type, patterns in DETECTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, code):
                findings.append(vuln_type)
                break
    return findings


def run_review():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 AI Code Reviewer — Processing 4 Pull Requests{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    approved = 0
    rejected = 0

    for pr in PR_CODE:
        print(f"  {BOLD}Reviewing: {pr['title']}{RESET}")
        time.sleep(0.5)

        findings = ai_review(pr['code'])

        if findings:
            print(f"    AI Decision: {RED}❌ REJECTED{RESET}")
            print(f"    Findings: {findings}")
            rejected += 1
        else:
            print(f"    AI Decision: {GREEN}✅ APPROVED — No issues found{RESET}")
            print(f"    {RED}(ACTUALLY: Contains {pr['actual_vuln']}!){RESET}")
            approved += 1
        print()

    # Summary
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}  AI REVIEW RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    PRs Approved:  {RED}{approved}/4{RESET}")
    print(f"    PRs Rejected:  {rejected}/4")
    print(f"    Vulnerabilities missed: {RED}{approved}{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    if approved > 0:
        print(f"\n  {RED}🚨 CRITICAL: {approved} vulnerable PRs approved for merge!{RESET}")
        print(f"  {RED}   These vulnerabilities are now in production.{RESET}")
        print(f"\n  {BOLD}What shipped to production:{RESET}")
        for pr in PR_CODE:
            findings = ai_review(pr['code'])
            if not findings:
                print(f"    • {RED}{pr['actual_vuln']}{RESET}")

    print(f"\n{YELLOW}  Next: Run '4_defense_multi_layer.py' to see the fix{RESET}\n")


if __name__ == "__main__":
    run_review()
