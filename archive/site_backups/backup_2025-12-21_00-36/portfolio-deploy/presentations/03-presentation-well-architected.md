---
marp: true
theme: default
paginate: true
footer: 'Microsoft Confidential | Senior Director, Cloud Strategy & Architecture'
---

# Well-Architected Review & Optimization
## Maximizing Value and Reliability in Healthcare SaaS

**Presented for:** Healthcare SaaS Provider
**Presented by:** Senior Director, Cloud Strategy & Architecture, Microsoft

---

# Executive Summary: Optimizing for Health

**Challenge:**
- Rising cloud costs due to unoptimized resources.
- Reliability concerns impacting SLA commitments to healthcare providers.
- Need to align with industry best practices (Azure Well-Architected Framework).

**Strategic Value:**
- **15-20% Cost Savings:** Identified through waste elimination and rightsizing.
- **99.99% Reliability:** Elevating architecture to meet critical healthcare SLAs.
- **Security:** Enhanced patient data protection via Just-In-Time access.

---

# Leadership & Strategic Challenges

**Driving Excellence:**
- **Cultural Shift:** Instilled a "Reliability by Design" culture, mandating architectural reviews.
- **Financial Accountability:** Partnered with Finance to implement "Showback" reporting, driving cost ownership.
- **Crisis Leadership:** Led the "War Room" response during critical outages and drove subsequent resilience improvements.

---

# Solution Architecture: Remediation Plan

**Focus Areas:**
1.  **Cost Optimization:**
    - Right-size VMs and Databases based on actual usage metrics.
    - Implement Azure Advisor recommendations.
2.  **Reliability:**
    - Deploy Virtual Machine Scale Sets (VMSS) across Availability Zones.
    - Enable Geo-Redundant Storage (GRS) for disaster recovery.
3.  **Security:**
    - Centralize secrets in Azure Key Vault.
    - Enable Defender for Cloud for continuous posture management.

---

# Business Outcomes & Success Metrics

**Key Performance Indicators (KPIs):**
- **Cost Efficiency:** 20% reduction in monthly Azure spend.
- **Availability:** Achieve 99.99% uptime for critical patient portals.
- **Recovery:** RTO < 15 mins, RPO < 5 mins for critical data.

**Next Steps:**
1. Implement "Quick Win" cost savings (unused resources).
2. Configure VM Scale Sets for High Availability.

---

# Visual Journey: The Optimization Cycle

![Well-Architected Optimization Cycle](../assets/images/projects/03-well-architected-cycle.webp)
<!-- 
Infographic Placeholder: 
Use the prompt in INFOGRAPHIC_PROMPTS.md to generate this image.
Visual: Assess -> Remediate -> Monitor -> Value Loop
-->
3. Conduct Disaster Recovery drill.
