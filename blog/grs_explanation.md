# Why GRS (Geo-Redundant Storage)?

In a **Regulator-Ready** architecture, data durability is a non-negotiable compliance requirement.

**GRS (Geo-Redundant Storage)** is selected because:
1.  **Region Survival**: If the entire primary region (UK South) goes dark (e.g., major physical disaster), your data (audit logs, training datasets, model artifacts) is already safely replicated to the secondary region (UK West).
2.  **RPO (Recovery Point Objective)**: It maximizes the chance of recovering recent data in a catastrophic failure scenario without manual backups.
3.  **Audit Compliance**: Regulators often require proof that "data exists in two geographically separated locations" to prevent total data loss.

It aligns with the **"Passive Cold" DR strategy** mentioned in the blog: compute is off in UK West (saving money), but **data** is always their (via SQL Geo-Replica and Storage GRS), ready to be attached to new compute instances immediately.
