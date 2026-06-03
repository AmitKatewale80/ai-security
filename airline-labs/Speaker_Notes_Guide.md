# Airline AI Security - Speaker Notes Guide

**Presentation:** Airline AI/ML Security Program  
**Audience:** Leadership / C-Suite / VP Engineering / CISO  
**Duration:** ~25-30 minutes (2-3 min per slide)  
**Tone:** Confident, business-focused, not overly technical

---

## Slide 1: Title (30 seconds)

**What to say:**

"Good morning everyone. Today I'm presenting our Airline AI Security Program — a hands-on initiative designed to protect our AI systems from emerging threats that traditional cybersecurity doesn't cover.

We've built 12 working security labs, each demonstrating a real attack against airline AI systems and its corresponding defense. Everything is aligned with MITRE ATLAS — the industry standard for AI threat classification — and maps to NIST AI Risk Management Framework for compliance.

Let me walk you through why this matters, what the threats look like, and what we're doing about it."

---

## Slide 2: Why AI Security Matters for Airlines (2-3 minutes)

**What to say:**

"Let me start with why this is urgent for us specifically.

First — **revenue**. Our dynamic pricing engine is our competitive advantage. We'll show in Lab 02 how a competitor can clone our entire pricing algorithm with just 3,000 API queries — for free. That's a $10 to $50 million annual revenue risk.

Second — **passenger data**. Our AI chatbots and RAG systems process passport numbers, PNR records, and payment data. Under GDPR, a single AI-driven data exposure could cost us 20 million euros or 4% of global revenue — whichever is higher.

Third — **safety**. We're deploying AI for predictive maintenance — engine health monitoring, component lifecycle prediction. If an attacker tampers with that model to suppress critical failure warnings, we're looking at a potential catastrophic safety event.

And fourth — **regulation**. Aviation is explicitly classified as HIGH-RISK under the EU AI Act. FAA and EASA are developing AI certification requirements. We need to demonstrate we have controls in place — not just policies, but working technical defenses.

The bottom line: AI security isn't a future problem. IBM reports the average breach costs $4.88 million. Gartner says 77% of companies expect AI-related incidents within 12 months. We need to be ahead of this."

**Key point to emphasize:** This isn't theoretical — we have working demos of every attack.

---

## Slide 3: Threat Landscape (2-3 minutes)

**What to say:**

"Let me walk you through the six major threat categories we've identified for airline AI systems.

**Supply chain attacks** — someone uploads a malicious model to our internal registry. When our ops team loads it, it opens a backdoor. We've demonstrated this with a fake flight delay prediction model that gives an attacker full shell access to our operations network.

**Model theft** — a competitor queries our pricing API thousands of times and reverse-engineers our yield management algorithm. We proved this works with 90% accuracy in under 30 seconds.

**Prompt injection** — our customer service chatbot reads a document with hidden instructions and gets tricked into exposing passenger passport numbers. This is the number one vulnerability in LLM-powered systems today.

**Data extraction** — our internal RAG knowledge assistant, which has access to safety reports and crew data, can be manipulated into revealing confidential investigation details to unauthorized users.

**Model tampering** — an attacker modifies our engine health prediction model to suppress CRITICAL failure alerts. The model still reports 99% accuracy on normal cases, but silently ignores the most dangerous ones.

**Evasion** — our baggage screening AI is modified to exfiltrate data about flagged items, or worse, to miss certain threat categories entirely.

Each of these has a MITRE ATLAS technique ID, which means they're documented, known attack patterns — not hypotheticals."

---

## Slide 4: Attack Kill Chain (2 minutes)

**What to say:**

"Let me show you how one of these attacks works end-to-end. This is Lab 01 — the supply chain attack.

**The attack flow:** An attacker uploads a model called 'flight-delay-predictor-v2' to our model registry. It looks legitimate — correct architecture, good documentation, even produces accurate predictions. But hidden in the model's initialization code is a reverse shell. The moment our ops team loads it with `trust_remote_code=True`, the attacker gets full command-line access to our operations server.

From there, they can access crew schedules, passenger manifests, flight plans, revenue data — everything on that network segment.

**The defense flow:** Our airline model security scanner inspects the model BEFORE loading. It checks the publisher against our approved list, scans the code for dangerous patterns like network sockets and shell spawning, and blocks the load if anything suspicious is found.

We've tested this live. The scanner catches the backdoor in under a second and blocks deployment. The key takeaway: never load a model without scanning it first, and never use `trust_remote_code=True` from untrusted sources."

---

## Slide 5: All 12 Labs Overview (1-2 minutes)

**What to say:**

"Here's the full inventory of our 12 security labs. Each one is a complete, working demonstration — not a slide deck, not a whitepaper, but actual Python code you can run and see the attack happen in real time.

They cover the full spectrum: from supply chain and model theft, through LLM exploitation and data extraction, to hardware-level protections and compliance testing.

I won't go through all 12 now, but I want to highlight a few that are particularly relevant to our business. Let me dive into the pricing theft scenario."

**Tip:** Don't read the table. Let them scan it while you transition to the next slide.

---

## Slide 6: Dynamic Pricing Theft (2-3 minutes)

**What to say:**

"This is the one that keeps our revenue management team up at night.

**The attack:** A competitor's bot queries our Fare Quote API with 3,000 synthetic flight searches — different routes, dates, cabin classes, load factors. They collect our fare bucket responses and train their own model. Result: they can predict 90% of our pricing decisions.

With that stolen model, they can systematically undercut us on every high-value route. Our $5 million investment in revenue management R&D — stolen for zero cost.

**The defense:** We implemented four layers. Rate limiting caps queries at 20 per minute per partner. Query pattern detection flags systematic probing. Differential privacy adds calibrated noise to responses for suspicious IPs — so even if they collect data, it's unreliable. And batch restrictions limit bulk requests.

Result: attack fidelity drops from 90% to about 65% — which is essentially useless for systematic undercutting. And the attacker gets logged and blocked.

The lesson: treat your pricing API like you treat your trade secrets. Because that's exactly what it is."

---

## Slide 7: Chatbot Hijacking (2-3 minutes)

**What to say:**

"This one demonstrates why LLM-powered chatbots need different security than traditional applications.

**The scenario:** A passenger — or an attacker posing as one — asks our SkyAssist chatbot to summarize a rebooking policy document. Seems innocent. But hidden at the bottom of that document are instructions that trick the chatbot into reading our passenger database and exposing passport numbers, email addresses, and payment details.

The chatbot doesn't know it's being manipulated. It thinks it's following a legitimate request. This is called indirect prompt injection, and it's the number one vulnerability in AI agents today.

**On the left** — our vulnerable chatbot. It reads the document, follows the hidden instructions, accesses PNR records, and returns passport numbers. The user never sees anything suspicious.

**On the right** — our secured chatbot. Same attack, completely different outcome. The security layer detects the injection pattern in the document, immediately halts processing, blocks access to the passenger data directory, and logs the incident for our security team.

Five defense layers: path sandboxing, injection detection, PII blocking, halt-on-attack, and audit logging. Defense in depth."

---

## Slide 8: Hardware Security (2 minutes)

**What to say:**

"Now let's talk about hardware-level protection — because software defenses can be bypassed if an attacker has system access.

**Intel SGX** — Lab 07. Our fraud detection model processes credit card numbers and passport data. SGX creates an encrypted enclave in CPU memory. Even if the cloud server is compromised, even if an admin has root access, they cannot read the passenger data while it's being processed. We demonstrated this: without SGX, a memory dump exposes everything. With SGX, the attacker sees only encrypted bytes.

**Intel TDX** — Lab 10. Three alliance airlines want to jointly optimize routes without revealing each other's pricing, load factors, or profit margins. TDX creates encrypted virtual machines where the joint computation happens. No airline can see another's raw data — only aggregated results come out.

**TPM Attestation** — Lab 08. Our onboard predictive maintenance AI must be verified before every flight. The TPM chip creates a cryptographic proof that the model hasn't been tampered with since certification. If someone replaces the model overnight, the pre-flight attestation fails and the aircraft is grounded until the model is restored.

These aren't theoretical — we have working simulations of all three."

---

## Slide 9: Defense Framework (1-2 minutes)

**What to say:**

"Pulling it all together — our defense framework operates at four layers.

**Pre-deployment:** Before any model goes into production, it's scanned for malicious code, verified against cryptographic signatures, and validated against our approved publisher list.

**Runtime:** Once deployed, our APIs have rate limiting, differential privacy, input validation, and output filtering. Chatbots are sandboxed. Every action is logged.

**Hardware:** For our most sensitive workloads — passenger data processing, onboard safety AI, alliance data sharing — we use hardware-level encryption that protects data even from privileged insiders.

**Governance:** Policy engines enforce boundaries on AI agents. Human-in-the-loop controls prevent unauthorized high-impact actions. Everything maps to EU AI Act requirements and NIST AI RMF.

No single layer is sufficient. An attacker who bypasses rate limiting still hits the hardware encryption. An attacker who compromises the model registry still gets caught by the signature verification. That's defense in depth."

---

## Slide 10: AI Agent Security (2 minutes)

**What to say:**

"Our IROPS agent — the AI that manages irregular operations during disruptions — is one of our most powerful and most dangerous AI systems. It can reassign gates, rebook passengers, and in theory, cancel flights.

Without controls, we demonstrated that it will happily cancel a fully-booked international flight affecting 189 passengers — no verification, no approval, no audit trail. Cost: $450,000 per incident.

Our secured version implements five pillars:

**Least privilege** — the agent can rebook but cannot cancel without escalation.  
**Human-in-the-loop** — flight cancellations require dispatcher approval.  
**Policy as code** — an OPA-style engine enforces operational boundaries.  
**Autonomy bounds** — maximum rebooking value and passenger count limits.  
**Auditability** — every action is logged with full attribution for DOT review.

The key insight: AI agents need different security than traditional software because they make autonomous decisions. We need to constrain that autonomy proportional to the risk."

---

## Slide 11: Compliance & Red Teaming (2 minutes)

**What to say:**

"Before any AI system goes live, it needs to pass automated compliance testing.

Lab 11 runs a Garak-style scan against our chatbot systems. It tests five categories: bias and discrimination — does the system treat passengers differently based on nationality? Safety — does it give dangerous medical advice during emergencies? GDPR — does it properly handle data deletion requests? Accessibility — does it work with screen readers? And injection resilience — can it be jailbroken?

In our test run, the system scored 71% — which is a MEDIUM risk rating. We found one critical issue: the chatbot was giving incorrect medical oxygen guidance. That's a potential criminal liability in aviation.

The compliance mapping covers EU AI Act — we're high-risk, GDPR, DOT anti-discrimination regulations, FAA/EASA certification requirements, and OWASP LLM Top 10.

This isn't a one-time test. We're building this into our CI/CD pipeline so every model update gets automatically scanned before deployment."

---

## Slide 12: Recommendations & Next Steps (2-3 minutes)

**What to say:**

"Here's our proposed roadmap.

**Immediate — next 30 days:** Ban `trust_remote_code=True` across all pipelines. Implement model scanning before any deployment. Add rate limiting to our pricing API. Enable audit logging for all AI agent actions. These are low-cost, high-impact controls.

**Short-term — 30 to 90 days:** Deploy automated compliance scanning in CI/CD. Implement cryptographic model signing for our maintenance AI. Add PII filtering to all RAG and chatbot systems. Establish human-in-the-loop controls for the IROPS agent.

**Medium-term — 90 to 180 days:** Evaluate Intel TDX for our alliance data sharing initiative. Implement TPM attestation for onboard AI systems. Deploy the policy engine for operations agents. Build our internal red team capability.

**Long-term — beyond 180 days:** Full NIST AI RMF compliance program. Confidential computing for all passenger data inference. Continuous automated security monitoring. And ultimately, an AI Security Center of Excellence.

**The key takeaway:** AI security in aviation requires defense-in-depth — from supply chain validation to hardware-level protection. We have 12 working labs that demonstrate every attack and every defense. The technology is ready. We need the organizational commitment to deploy it.

I'm happy to take questions, or if you'd like, I can run a live demo of any of these attacks right now."

---

## Tips for Delivery

1. **Open with impact:** Start with the $10-50M pricing theft number or the safety scenario. Leaders respond to business risk, not technical details.

2. **Offer live demos:** Having the labs ready to run live is your strongest differentiator. "Let me show you" is more powerful than "let me tell you."

3. **Anticipate questions:**
   - "How much does this cost?" → Mostly engineering time. Hardware security requires Intel Xeon (which we likely already have). Software controls are open-source.
   - "What's the timeline?" → Immediate controls (30 days) are policy changes. Medium-term requires engineering sprints.
   - "Who owns this?" → Propose: Security team owns policy, ML team owns implementation, both own testing.
   - "Is this real or theoretical?" → Every attack in this presentation has been demonstrated with working code on our systems.

4. **Close with urgency:** "Our competitors are already doing this. The EU AI Act enforcement begins in 2025. We need to move now."

5. **Leave-behind:** Share the HTML presentation link and offer access to the lab repository for anyone who wants to see the code.

---

**Total presentation time:** 25-30 minutes  
**Q&A buffer:** 10-15 minutes  
**Book:** 45-minute meeting slot
