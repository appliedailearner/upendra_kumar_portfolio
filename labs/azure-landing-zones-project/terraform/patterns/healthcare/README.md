# Healthcare Pattern - HIPAA Compliant Azure Landing Zone

This pattern deploys Azure landing zones configured for Healthcare organizations with HIPAA compliance requirements.

## Features

- ✅ HIPAA-compliant infrastructure
- ✅ PHI data protection
- ✅ 7-year audit log retention
- ✅ Enhanced encryption (CMK mandatory)
- ✅ Session recording for all access
- ✅ BAA compliance controls

## Usage

```hcl
# Healthcare-specific AI Landing Zone
module "ai_landing_zone" {
  source = "../../modules/ai-landing-zone"

  resource_group_name = "rg-prod-eus2-healthcare-ai-01"
  location            = "eastus2"
  environment         = "prod"
  vnet_address_space  = ["10.100.0.0/16"]
  
  # HIPAA Compliance
  industry_compliance = {
    pci_dss = false
    hipaa   = true    # HIPAA enabled
    sox     = false
    gdpr    = true
  }
  
  cost_tier = "premium"  # Premium for HIPAA
  
  # Enhanced security for PHI
  log_analytics_retention_days = 2555  # 7 years
  
  tags = {
    Environment = "Production"
    Industry    = "Healthcare"
    Compliance  = "HIPAA,HITECH"
    DataClass   = "PHI"
  }
}

# Healthcare AVD with session recording
module "avd_landing_zone" {
  source = "../../modules/avd-landing-zone"

  resource_group_name = "rg-prod-eus2-healthcare-avd-01"
  location            = "eastus2"
  environment         = "prod"
  vnet_address_space  = ["10.200.0.0/16"]
  
  compliance = {
    session_recording = true   # Mandatory for HIPAA
    mfa_required     = true
  }
  
  tags = {
    Environment = "Production"
    Industry    = "Healthcare"
    Compliance  = "HIPAA"
  }
}
```

## HIPAA-Specific Policies

### Required Policies
1. **164.312(a)(2)(iv)** - Encryption and Decryption
   - Customer-managed keys (CMK) mandatory
   - TLS 1.3 for data in transit

2. **164.312(b)** - Audit Controls
   - 7-year log retention
   - Immutable audit logs

3. **164.312(c)(1)** - Integrity Controls
   - Data integrity validation
   - Tamper detection

4. **164.312(d)** - Person or Entity Authentication
   - MFA mandatory
   - Conditional Access policies

## Deployment

```bash
cd terraform/patterns/healthcare
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Cost Estimate

**Monthly Cost (Healthcare Configuration)**:
- AI Landing Zone (Premium): $25,000
- AVD with session recording: $12,000
- Enhanced logging (7 years): $2,500
- **Total**: ~$39,500/month

## Compliance Checklist

- [ ] BAA signed with Microsoft
- [ ] HIPAA Security Rule assessment completed
- [ ] Privacy Rule compliance verified
- [ ] Breach notification procedures documented
- [ ] PHI data classification implemented
- [ ] Access controls configured
- [ ] Audit logging enabled (7 years)
- [ ] Encryption at rest and in transit
- [ ] Incident response plan documented

## References

- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/)
- [Azure HIPAA Compliance](https://learn.microsoft.com/azure/compliance/offerings/offering-hipaa-us)
- [PHI Data Protection](https://www.hhs.gov/hipaa/for-professionals/privacy/)
