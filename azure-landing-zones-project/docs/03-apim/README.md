# API Management (APIM) - Complete Documentation Package

**Project**: Azure Landing Zones - Financial Services  
**Component**: API Management (APIM)  
**Version**: 1.0.0  
**Last Updated**: December 2025

---

## 1. Design Decisions

### APIM SKU Selection: Premium Tier

**Rationale**:
- Multi-region deployment capability
- VNet integration for private connectivity
- Unlimited caching and higher throughput
- Required for Financial Services compliance

**Configuration**:
- **SKU**: Premium
- **Units**: 2 (primary region), 1 (secondary region)
- **Regions**: East US 2 (primary), West US 2 (secondary)
- **Capacity**: 4,000 requests/second

---

## 2. Architecture Overview

### Network Design
```
Internet/Partners
    ↓
Application Gateway (WAF)
    ↓
APIM (Internal VNet Mode)
    ├── Developer Portal (Private)
    ├── Gateway (Private Endpoint)
    └── Management API (Private)
    ↓
Backend Services
    ├── Azure Functions
    ├── AKS Microservices
    ├── Logic Apps
    └── On-Premises APIs (ExpressRoute)
```

### Key Components
- **API Gateway**: Internal VNet deployment
- **Developer Portal**: Self-service API documentation
- **Azure AD B2C**: External partner authentication
- **Application Insights**: API monitoring and analytics
- **Azure Key Vault**: API keys and certificates

---

## 3. API Security

### Authentication & Authorization

**Internal APIs**:
- Azure AD OAuth 2.0
- Managed identities for service-to-service
- JWT token validation

**External APIs**:
- Azure AD B2C for partners
- API subscription keys
- IP whitelisting
- Rate limiting

**Security Policies**:
```xml
<policies>
    <inbound>
        <validate-jwt header-name="Authorization">
            <openid-config url="https://login.microsoftonline.com/{tenant}/.well-known/openid-configuration" />
            <audiences>
                <audience>api://financial-services-api</audience>
            </audiences>
        </validate-jwt>
        <rate-limit-by-key calls="100" renewal-period="60" counter-key="@(context.Subscription.Id)" />
        <ip-filter action="allow">
            <address-range from="10.0.0.0" to="10.255.255.255" />
        </ip-filter>
    </inbound>
</policies>
```

---

## 4. API Design

### API Categories

**Customer APIs**:
- Account Management API
- Transaction API
- Payment Processing API
- Customer Profile API

**Partner APIs**:
- Credit Bureau Integration
- Payment Gateway Integration
- Third-Party Data Providers

**Internal APIs**:
- Fraud Detection API
- Risk Assessment API
- Compliance Reporting API

### API Versioning Strategy
- URL path versioning: `/v1/`, `/v2/`
- Backward compatibility maintained for 12 months
- Deprecation notices 6 months in advance

---

## 5. Bill of Materials

### Monthly Costs

| Resource | SKU | Quantity | Monthly Cost (USD) |
|----------|-----|----------|-------------------|
| APIM Premium | 2 units (primary) | 1 | $3,600 |
| APIM Premium | 1 unit (secondary) | 1 | $1,800 |
| Application Gateway | WAF v2 | 1 | $350 |
| Application Insights | 100 GB/month | 1 | $230 |
| Azure AD B2C | 50K MAU | 1 | $0 (free tier) |
| Key Vault | Premium | 1 | $25 |
| **Total Monthly** | | | **$6,005** |

---

## 6. Detailed Configuration

### APIM Instance Setup

**Terraform Configuration**:
```hcl
resource "azurerm_api_management" "apim" {
  name                = "apim-prod-eus2-01"
  location            = "eastus2"
  resource_group_name = "rg-prod-eus2-apim-01"
  publisher_name      = "Financial Services Organization"
  publisher_email     = "api-admin@contoso.com"
  
  sku_name = "Premium_2"
  
  virtual_network_type = "Internal"
  virtual_network_configuration {
    subnet_id = azurerm_subnet.apim.id
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  protocols {
    enable_http2 = true
  }
  
  security {
    enable_backend_ssl30  = false
    enable_backend_tls10  = false
    enable_backend_tls11  = false
    enable_frontend_ssl30 = false
    enable_frontend_tls10 = false
    enable_frontend_tls11 = false
  }
}
```

### API Policy Templates

**Rate Limiting Policy**:
```xml
<rate-limit-by-key calls="1000" 
                   renewal-period="60" 
                   counter-key="@(context.Subscription.Id)" />
```

**Caching Policy**:
```xml
<cache-lookup vary-by-developer="false" 
              vary-by-developer-groups="false" 
              downstream-caching-type="none">
    <vary-by-query-parameter>id</vary-by-query-parameter>
</cache-lookup>
```

**Transformation Policy**:
```xml
<set-header name="X-Correlation-Id" exists-action="override">
    <value>@(Guid.NewGuid().ToString())</value>
</set-header>
<set-backend-service base-url="https://backend-api.contoso.com" />
```

---

## 7. Monitoring & Operations

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Availability | 99.95% | < 99.9% |
| Response Time (P95) | < 500ms | > 1000ms |
| Error Rate | < 0.1% | > 1% |
| Throughput | 4000 req/s | > 3500 req/s |

### Dashboards
- **API Analytics**: Request volume, response times, errors
- **Developer Portal**: API usage by subscription
- **Backend Health**: Backend service availability
- **Security**: Failed authentication attempts, rate limit violations

### Alerting
```bash
# Create availability alert
az monitor metrics alert create \
  --name "APIM-Availability-Alert" \
  --resource-group rg-prod-eus2-apim-01 \
  --scopes /subscriptions/{sub-id}/resourceGroups/rg-prod-eus2-apim-01/providers/Microsoft.ApiManagement/service/apim-prod-eus2-01 \
  --condition "avg Availability < 99.9" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action email api-ops@contoso.com
```

---

## 8. Disaster Recovery

### DR Strategy
- **Primary Region**: East US 2
- **Secondary Region**: West US 2
- **Failover**: Automatic via Traffic Manager
- **RPO**: 1 hour (configuration sync)
- **RTO**: 15 minutes (DNS propagation)

### Backup & Restore
```powershell
# Backup APIM configuration
Backup-AzApiManagement `
  -ResourceGroupName "rg-prod-eus2-apim-01" `
  -Name "apim-prod-eus2-01" `
  -StorageContext $storageContext `
  -TargetContainerName "apim-backups" `
  -TargetBlobName "apim-backup-$(Get-Date -Format 'yyyyMMdd').apimbackup"
```

---

## 9. Operational Procedures

### Common Tasks

**Add New API**:
1. Define OpenAPI specification
2. Import to APIM via portal or CLI
3. Configure policies (auth, rate limiting, caching)
4. Test in development environment
5. Publish to production
6. Update developer portal documentation

**Rotate API Keys**:
```bash
# Regenerate subscription key
az apim subscription update \
  --resource-group rg-prod-eus2-apim-01 \
  --service-name apim-prod-eus2-01 \
  --sid <subscription-id> \
  --primary-key <new-key>
```

**Scale APIM**:
```bash
# Add capacity unit
az apim update \
  --name apim-prod-eus2-01 \
  --resource-group rg-prod-eus2-apim-01 \
  --sku-capacity 3
```

### Troubleshooting

**Issue**: High latency on API calls  
**Solution**:
1. Check Application Insights for slow backend calls
2. Review caching policies
3. Verify backend service health
4. Check network connectivity

**Issue**: Authentication failures  
**Solution**:
1. Validate JWT token configuration
2. Check Azure AD app registration
3. Verify token expiration settings
4. Review APIM diagnostic logs

---

## 10. Compliance & Governance

### PCI-DSS Requirements
- ✓ TLS 1.2+ enforced
- ✓ API keys stored in Key Vault
- ✓ All API calls logged
- ✓ Network segmentation via VNet
- ✓ Regular security scans

### SOC 2 Controls
- ✓ Access control via Azure AD
- ✓ Audit logging enabled
- ✓ Encryption in transit and at rest
- ✓ Change management process
- ✓ Incident response procedures

### Azure Policy Assignments
- Require HTTPS for APIs
- Enforce minimum TLS version
- Require diagnostic logging
- Block public network access
- Require private endpoints

---

## 11. Support & Handover

### Support Contacts
- **L1 Support**: api-support@contoso.com (24/7)
- **L2 Support**: api-ops@contoso.com (24/7)
- **L3 Engineering**: apim-engineering@contoso.com (8/5)

### Escalation Path
1. L1 Support (ServiceNow) → 15 minutes
2. L2 API Operations → 30 minutes
3. L3 Engineering Team → 1 hour
4. Platform Architect → 2 hours

### Known Issues
| Issue | Workaround | Target Fix |
|-------|------------|------------|
| Occasional 502 errors | Retry logic in client | Q1 2026 |
| Developer portal slow load | Clear browser cache | Q2 2026 |

---

## References
- [Azure APIM Documentation](https://learn.microsoft.com/azure/api-management/)
- [APIM Policies Reference](https://learn.microsoft.com/azure/api-management/api-management-policies)
- [APIM Security Best Practices](https://learn.microsoft.com/security/benchmark/azure/baselines/api-management-security-baseline)

---

**Document Owner**: API Platform Architect  
**Status**: Production Ready  
**Last Review**: December 2025  
**Next Review**: March 2026
