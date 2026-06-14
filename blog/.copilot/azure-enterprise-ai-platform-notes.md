# Enterprise Azure AI Platform Diagram Notes

## Narrative
- Users enter through one governed control plane.
- The platform separates `Chat Lane` and `Ingestion Lane` for leadership clarity.
- Shared enterprise controls stay centralized.
- Private data and AI services are shown as a compact dependency cluster.
- UAE Central is positioned as `Warm Standby DR`, not as a misleading full active-active copy.

## Deliberate fixes from the audit
- Replaced the infrastructure-heavy view with a leadership-first story.
- Kept one compact shared-controls section instead of full subnet drawings.
- Made DNS and private access explicit through `DNS Private Resolver`, `Private DNS`, and `Private Endpoints`.
- Corrected DR semantics:
  - `AI Gateway` sync is configuration and failover readiness.
  - `DR Runtime` represents warm standby redeployability, not platform replication.
  - `DR Data Services` represents service-native recovery patterns.
- Reduced repeated low-level landing zone detail.

## Edge semantics
- Solid blue: active request path.
- Solid teal: private service and control-plane access.
- Dashed purple: synchronization, replication, or failover readiness.
