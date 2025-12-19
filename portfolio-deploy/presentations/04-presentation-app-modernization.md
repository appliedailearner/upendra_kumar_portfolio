---
marp: true
theme: gaia
class: invert
paginate: true
footer: 'Upendra Kumar - Azure Solutions Architect | Leadership Portfolio'
---

<!-- style
section {
  background-color: #0a0a0f;
  color: #f8fafc;
}
h1, h2 {
  color: #0078D4;
}
footer {
  color: #cbd5e1;
}
-->

# Application Modernization Blueprint
## Scaling Retail Operations for the Digital Era

**Presented for:** Retail Enterprise
**Presented by:** Senior Director, Cloud Strategy & Architecture, Microsoft

---

# Executive Summary: Ready for Peak Season

**Challenge:**
- Legacy on-premise apps struggling to handle peak traffic (e.g., Black Friday).
- Slow, manual quarterly deployment cycles hindering innovation.
- High operational overhead for maintaining servers.

**Strategic Value:**
- **Elastic Scalability:** Auto-scale to handle traffic spikes without CapEx.
- **Daily Deployments:** Shift from quarterly to daily releases via CI/CD.
- **Performance:** 50% improvement in page load times for better UX.

---

# Leadership & Strategic Challenges

**Transforming Delivery:**
- **DevOps Adoption:** Overcame resistance to automation by demonstrating 90% error reduction in pilots.
- **Business Continuity:** Orchestrated "Black Friday" readiness across infrastructure and application teams.
- **Vendor Management:** Managed 3rd-party integrations to ensure compatibility with cloud-native architecture.

---

# Solution Architecture: Cloud-Native PaaS

**Core Components:**
- **App Service (PaaS):** Fully managed web hosting with built-in autoscaling.
- **Azure SQL Database:** Managed relational database with high availability.
- **Azure Front Door:** Global load balancing and content delivery (CDN).
- **DevOps:** GitHub Actions / Azure DevOps for automated CI/CD pipelines.

**Modernization Steps:**
- **Rehost:** Migrate .NET apps to App Service.
- **Refactor:** Upgrade to .NET 6+; implement Redis Cache for session state.

---

# Business Outcomes & Success Metrics

**Key Performance Indicators (KPIs):**
- **Performance:** < 2 second page load time globally.
- **Agility:** Deployment frequency increased from 4/year to On-Demand.
- **Reliability:** Zero downtime during peak sales events.

**Next Steps:**
1. Setup Azure DevOps pipelines.
2. Deploy "Staging" environment in App Service.
3. Perform load testing to validate autoscaling.

---

# Visual Journey: The Modernization Path

![App Modernization Multi-Stage Delivery](../images/projects/04-app-modernization.png)

---
# Thank You
## Let's Build the Future of Cloud Together
**Upendra Kumar**
Azure Solutions Architect
upendra25312@gmail.com
[Portfolio Site](https://appliedailearner.github.io/upendra_kumar_portfolio/)
