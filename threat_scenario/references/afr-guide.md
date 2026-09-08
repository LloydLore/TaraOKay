# Attack Feasibility Rating (AFR) Scoring Guide - ISO 21434

This document provides detailed guidance for assessing attack feasibility using the AFR (Attack Feasibility Rating) methodology used by this repository's `threat_scenario` skill.

---

## Introduction

**Attack Feasibility Rating (AFR)** quantifies how difficult it is for an attacker to successfully execute a given threat scenario. Unlike impact assessment (which measures the consequences of a successful attack), AFR measures the effort, resources, and conditions required for the attack to succeed.

In this repository, AFR is calculated by scoring **5 independent factors** on a 0-3 scale, then summing them to produce a total score of 0-15. This total score maps to one of four repository-standard feasibility bands: Very Low, Low, Moderate, or High.

**Key Principle**: AFR is attacker-centric. It answers: "How easy is this attack for a motivated attacker with realistic resources?"

---

## AFR Calculation Methodology

### The 5 AFR Factors

Each threat scenario is scored across five dimensions:

1. **Elapsed Time**: How long does the attack take to execute (from planning to completion)?
2. **Specialist Expertise**: What level of technical skill does the attacker need?
3. **Knowledge of Item**: What information about the vehicle system must the attacker possess?
4. **Window of Opportunity**: How long does the attacker need access to the target?
5. **Equipment**: What tools, hardware, or software does the attacker require?

Each factor is scored **independently** on a 0-3 scale, where:
- **0** = Most difficult for attacker (highest barrier)
- **3** = Easiest for attacker (lowest barrier)

**Total AFR Score** = Sum of 5 factors (range: 0-15)

---

## Factor Scoring Tables

### Factor 1: Elapsed Time

**Question**: "How long does it take to plan and execute the attack?"

| Score | Elapsed Time | Description |
|-------|--------------|-------------|
| **0** | **> 6 months** | Long-term campaign requiring sustained effort over many months |
| **1** | **1-6 months** | Extended effort requiring weeks to months of preparation and execution |
| **2** | **1 week - 1 month** | Moderate effort requiring days to weeks |
| **3** | **< 1 week** | Rapid execution with minimal preparation |

**Examples**:
- Score 0: Reverse engineering proprietary ECU firmware (8-12 months), developing zero-day RTOS exploit (6+ months)
- Score 1: Fuzzing OTA protocol to find vulnerabilities (2-3 months), social engineering campaign (1-2 months)
- Score 2: Exploiting known CVE with public PoC (1-2 weeks), brute-forcing weak Bluetooth PIN (1 week)
- Score 3: Plug-and-play CAN injection tool (minutes), using default credentials (seconds), key fob relay (hours)

**Scoring Guidelines**:
- Count TOTAL time from initial reconnaissance to successful attack completion
- Include preparation time (research, tool setup) + execution time (actual attack)
- If attack can be repeated faster after initial success, score the FIRST attempt
- Parallel work (multiple attackers) does NOT reduce time score
- Consider realistic attacker (not theoretical maximum speed)

---

### Factor 2: Specialist Expertise

**Question**: "What level of technical skill does the attacker need to possess?"

| Score | Expertise Level | Description |
|-------|-----------------|-------------|
| **0** | **Multiple experts with rare skills** | Requires a team of specialists with deep, rare expertise in multiple domains |
| **1** | **Expert in automotive cybersecurity** | Single highly skilled individual with specialized automotive security knowledge |
| **2** | **Proficient IT/cybersecurity professional** | General IT security skills applicable to automotive (no automotive-specific expertise required) |
| **3** | **Layman / script kiddie** | No specialized skills required; can be executed by non-technical person or using ready-made tools |

**Examples**:
- Score 0: Bypassing HSM with side-channel analysis + custom RTOS exploit (cryptography PhD + automotive ECU expert + exploit developer)
- Score 1: Reverse engineering CAN protocol implementation, exploiting ECU bootloader, developing custom diagnostic tools
- Score 2: Exploiting web vulnerabilities in backend API, SQL injection in telematics server, using off-the-shelf pentesting tools
- Score 3: Using publicly available exploit code, following step-by-step tutorial, plug-and-play attack hardware from online marketplace

**Scoring Guidelines**:
- Score based on MINIMUM skill level required (not the skill of a sophisticated attacker)
- "Expert" means 5+ years specialized experience in automotive cybersecurity
- "Proficient" means general IT security background (CISSP, CEH, etc.)
- "Layman" means someone who can follow instructions but has no security training
- If a ready-made tool exists that automates the attack, score as 3
- If the attack requires understanding proprietary protocols, score as 0-1

---

### Factor 3: Knowledge of Item

**Question**: "What information about the vehicle system does the attacker need to know?"

| Score | Knowledge Required | Description |
|-------|-------------------|-------------|
| **0** | **Restricted / classified** | Information protected by NDA, classified, or insider-only access; requires espionage or insider threat |
| **1** | **Confidential / limited access** | Information not publicly available but obtainable with effort (supplier documentation, leaked internal docs, reverse engineering) |
| **2** | **Public with effort** | Information publicly available but requires research, reverse engineering, or specialized knowledge to interpret |
| **3** | **Publicly available / common knowledge** | Information freely accessible via public documentation, standards, or generic automotive knowledge |

**Examples**:
- Score 0: ECU bootloader signing keys, HSM architecture details, OEM-proprietary CAN message formats (not reverse-engineerable), cryptographic key derivation algorithms
- Score 1: Diagnostic tool protocols (obtained via supplier leak), ECU firmware (extracted via JTAG), OTA server API endpoints (discovered via reconnaissance)
- Score 2: ISO 15765 (CAN diagnostic protocol), publicly documented OTA update mechanisms, open-source RTOS internals, automotive CVE advisories
- Score 3: OBD-II port pinout (ISO 15031), Bluetooth pairing flow (Bluetooth SIG spec), USB Mass Storage protocol, default passwords in user manual

**Scoring Guidelines**:
- Score based on AVAILABILITY of information (not complexity of understanding)
- If the information can be reverse-engineered from a purchasable vehicle, score as 1-2
- If the information is in ISO/SAE standards or public research papers, score as 2-3
- If the information requires insider access (employee, supplier), score as 0
- If multiple pieces of information are needed, score the HARDEST to obtain

---

### Factor 4: Window of Opportunity

**Question**: "How much time does the attacker need physical/network access to execute the attack?"

| Score | Access Window | Description |
|-------|---------------|-------------|
| **0** | **Very narrow / restricted** | Extremely limited access window; requires physical access to restricted area; very short time available |
| **1** | **Moderate access window** | Limited but realistic access; requires coordination or specific conditions |
| **2** | **Easy access / extended time** | Readily available access for extended period; no special conditions |
| **3** | **Unlimited / always accessible** | No physical access required; remote attack; or permanent access |

**Examples**:
- Score 0: ECU removal from locked vehicle (minutes), JTAG probe connection during brief service visit, accessing backend server during narrow maintenance window
- Score 1: OBD-II port access while owner is away (30-60 minutes), USB port access during car wash, Bluetooth pairing when driver is nearby (5-10 minutes)
- Score 2: OBD-II port in parked vehicle (hours), WiFi connection when parked at home (overnight), USB port accessible to owner/driver (days)
- Score 3: OTA server accessible via internet (24/7), cellular telematics link (always on), Bluetooth interface (always discoverable), malicious companion app (always installed)

**Scoring Guidelines**:
- Score based on DURATION of access required (not frequency of opportunity)
- Remote attacks (no physical access) always score 3
- If attack requires multiple access sessions, sum the total time
- Consider realistic access scenarios (e.g., valet parking, service center)
- Physical access to vehicle interior (OBD-II, USB) typically scores 1-2
- Physical access requiring vehicle disassembly (ECU removal) scores 0

---

### Factor 5: Equipment

**Question**: "What tools, hardware, or software does the attacker need to acquire?"

| Score | Equipment Required | Description |
|-------|-------------------|-------------|
| **0** | **Bespoke / custom-built** | One-of-a-kind custom equipment requiring significant engineering effort to design and build |
| **1** | **Specialized but purchasable** | Automotive-specific professional tools available for purchase (expensive, limited availability) |
| **2** | **Standard automotive tools** | Common automotive repair/diagnostic equipment available to mechanics |
| **3** | **Off-the-shelf consumer electronics** | Standard consumer devices with no automotive-specific requirements |

**Examples**:
- Score 0: Custom FPGA-based CAN/Ethernet tap with nanosecond timing (months to build), custom side-channel analysis rig (RF probes + oscilloscope + software), lab-grade automotive fault injection equipment
- Score 1: Vector CANoe/CANalyzer ($5,000-$10,000), JTAG debugger for ARM Cortex ($500-$1,000), automotive diagnostic scanner ($1,000+), spectrum analyzer for RF analysis
- Score 2: Generic OBD-II scanner ($50-$200), multimeter, basic CAN adapter, USB cable, laptop with automotive software
- Score 3: Smartphone, standard laptop, Bluetooth adapter, USB flash drive, WiFi router, Amazon/eBay commodity electronics (<$100)

**Scoring Guidelines**:
- Score based on COST and AVAILABILITY (not complexity of use)
- If the equipment costs >$5,000, score as 0-1
- If the equipment is sold on Amazon/eBay for <$100, score as 3
- Software-only attacks using standard laptop score as 3
- If custom hardware fabrication is required (PCB design, FPGA programming), score as 0
- Stolen/leaked equipment (e.g., OEM diagnostic tools) scores as 1 (limited availability)

---

## AFR Total Score and Rating Bands

### Summation Formula

```
AFR Score = (Elapsed Time) + (Specialist Expertise) + (Knowledge of Item) + (Window of Opportunity) + (Equipment)
```

**Range**: 0 (most difficult for attacker) to 15 (easiest for attacker)

### AFR Rating Levels

After calculating the total AFR score (0-15), map it to a rating level:

| Total Score | AFR Rating | Interpretation for Attacker | Interpretation for Defender |
|-------------|------------|----------------------------|----------------------------|
| **0 - 4** | **Very Low** | Attack is very difficult (0) to difficult (4); significant barriers | **Lower risk** - attacker faces major obstacles |
| **5 - 9** | **Low** | Attack requires moderate effort and resources | **Medium risk** - skilled attacker can succeed |
| **10 - 13** | **Moderate** | Attack has lower barriers; accessible to skilled attackers | **Higher risk** - more accessible to attackers |
| **14 - 15** | **High** | Attack has minimal barriers; easily executable | **Very high risk** - easily exploitable |

**Repository terminology rule**:
- Lower AFR scores = harder for attacker = better security posture
- Higher AFR scores = easier for attacker = worse security posture
- Always describe bands as attacker feasibility: `Very Low / Low / Moderate / High`

---

## Downstream Use of AFR

`threat_scenario` owns AFR scoring only.

Downstream skills may combine AFR with impact or treatment logic, but those calculations are **out of scope for this reference**. In particular:
- `risk_treatment` owns Risk Value (RV) and treatment selection
- `attack_tree` owns path aggregation and effective AFR across multi-step paths

Use this document to score **individual threat scenarios** consistently. Do not use it to choose treatments.

---

## Worked Examples

### Example 1: CAN Bus Message Injection via OBD-II Port

**Threat Scenario**: Attacker with physical access to OBD-II port injects malicious CAN frames to manipulate vehicle behavior.

| Factor | Score | Justification |
|--------|-------|---------------|
| **Elapsed Time** | 3 | Attack executes in minutes once CAN adapter is connected to OBD-II port |
| **Specialist Expertise** | 2 | Requires understanding of CAN protocol and message format (proficient IT security professional) |
| **Knowledge of Item** | 3 | OBD-II pinout and CAN protocol are publicly documented (ISO 15765, ISO 15031) |
| **Window of Opportunity** | 2 | Requires 5-10 minutes physical access to OBD-II port in vehicle cabin (easily achievable in parked vehicle) |
| **Equipment** | 3 | $50 CAN bus adapter from Amazon + laptop with free CAN software |
| **Total AFR** | **13** | **Low (AFR rating)** |

**Interpretation**: This attack scores AFR=13 (AFR rating: Low). The low barriers to equipment and knowledge make it relatively accessible, but the need for physical access and some technical expertise still impose some friction.

---

### Example 2: Malicious OTA Update via Compromised Backend Server

**Threat Scenario**: Attacker compromises OTA backend server to push malicious firmware to vehicles remotely.

| Factor | Score | Justification |
|--------|-------|---------------|
| **Elapsed Time** | 1 | Requires 1-3 months to discover backend vulnerabilities, develop exploit, and test firmware injection |
| **Specialist Expertise** | 2 | Requires general web application security skills (SQL injection, API exploits) - no automotive-specific knowledge |
| **Knowledge of Item** | 1 | Requires reconnaissance to discover OTA server endpoints and authentication mechanisms (not public, but obtainable) |
| **Window of Opportunity** | 3 | OTA backend server is internet-accessible 24/7 (unlimited access for remote attacker) |
| **Equipment** | 3 | Off-the-shelf consumer electronics (standard laptop + web pentesting tools like Burp Suite, SQLMap - all freely available) |
| **Total AFR** | **10** | **Low (AFR rating)** |

**Interpretation**: This attack scores AFR=10 (AFR rating: Low). The internet-accessible attack surface and standard equipment lower some barriers, but the extended time and research required still create meaningful difficulty.

---

### Example 3: HSM Key Extraction via Side-Channel Power Analysis

**Threat Scenario**: Attacker extracts cryptographic keys from Hardware Security Module (HSM) using differential power analysis.

| Factor | Score | Justification |
|--------|-------|---------------|
| **Elapsed Time** | 0 | Requires > 6 months to set up lab environment, perform thousands of power measurements, and analyze statistical data |
| **Specialist Expertise** | 0 | Requires team of experts: cryptography PhD + hardware security specialist + automotive ECU expert |
| **Knowledge of Item** | 0 | HSM architecture and cryptographic implementation are OEM-proprietary (not reverse-engineerable without insider access) |
| **Window of Opportunity** | 0 | Requires ECU physical removal, lab setup with controlled power supply, and repeated access (extremely narrow window) |
| **Equipment** | 0 | Custom oscilloscope probes, RF-shielded chamber, high-resolution ADC, statistical analysis software (>$50,000 equipment cost) |
| **Total AFR** | **0** | **High** |

**Interpretation**: This attack scores AFR=0 (all factors at maximum difficulty for the attacker). A score of 0 sits in the **Very Low feasibility** band and represents an extremely difficult attack requiring extraordinary resources.

---

## AFR Rating Band Definitions

**IMPORTANT**: AFR uses a 0-15 scoring range with the following repository-standard feasibility bands:

| Total AFR Score | Rating Level | Attack Difficulty for Attacker |
|-----------------|--------------|--------------------------------|
| **0-4** | **Very Low** | Very difficult (score 0) to difficult (score 4); significant barriers |
| **5-9** | **Low** | Moderate difficulty; balanced effort required |
| **10-13** | **Moderate** | Lower barriers; accessible to skilled attackers |
| **14-15** | **High** | Minimal barriers; easily executable |

**Understanding the Score Direction**:
- **Lower scores (0-4)** = Higher difficulty for attacker (more barriers, longer time, rare expertise)
- **Higher scores (10-15)** = Lower difficulty for attacker (fewer barriers, shorter time, common tools)

Within each band, lower scores indicate greater attack difficulty. For example:
- AFR 0 (extremely difficult) vs AFR 4 (difficult but more feasible)
- AFR 10 (challenging) vs AFR 13 (more accessible)
- AFR 14 vs AFR 15 (both easy, slight variation)

---

## Summary and Best Practices

### Scoring Workflow

1. **Score each factor independently** (0-3 scale)
2. **Sum the 5 factors** to get total AFR score (0-15)
3. **Map total to rating band** (Very Low/Low/Moderate/High)
4. **Record the 5 factor justifications** so downstream reviewers can audit the score
5. **Hand off to downstream skills** for attack-tree aggregation or risk-treatment calculations if needed

### Key Reminders

- AFR is **attacker-centric**: "How easy is this for the attacker?"
- Score **realistically**: Assume motivated, skilled attacker with time and resources
- Score **conservatively**: When uncertain between two scores, choose the EASIER for attacker (higher score)
- AFR is **independent of impact**: Rate feasibility separately from consequences
- **Higher AFR numeric score (10-15)** means higher risk to defender (attack is easier to execute)
- **Lower AFR numeric score (0-4)** means lower risk to defender (attack is very difficult)
- **Rating band "Very Low" (0-4)** = very high difficulty FOR ATTACKER = lower risk for defender
- **Rating band "High" (14-15)** = low difficulty FOR ATTACKER = higher risk for defender

### Common Pitfalls

- ❌ Scoring expertise based on YOUR team's skills (score based on ATTACKER's skills)
- ❌ Assuming attackers lack resources (assume realistic motivated threat actor)
- ❌ Confusing rating bands with numeric scores ("Very Low (0-4)" means VERY LOW feasibility for attacker = LOWER risk for defender)
- ❌ Confusing "higher AFR score" (14-15 = easier attack = higher risk) with the feasibility label ("High" means HIGH attacker feasibility, not high attacker difficulty)
- ❌ Scoring optimistically ("our system is secure, so score 0") - score realistically
- ❌ Averaging factors instead of summing

---

**End of AFR Scoring Guide**
