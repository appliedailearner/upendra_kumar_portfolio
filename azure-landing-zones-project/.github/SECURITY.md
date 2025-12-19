# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **[Your Security Email]**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information (as much as you can provide) to help us better understand the nature and scope of the possible issue:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

## Preferred Languages

We prefer all communications to be in English.

## Security Update Process

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new security patch versions as soon as possible

## Security Best Practices

When using this Azure Landing Zones project:

### 1. Secrets Management
- **Never commit secrets** to the repository
- Use Azure Key Vault for all secrets
- Use managed identities where possible
- Rotate secrets regularly

### 2. Network Security
- Deploy all resources with private endpoints
- Use Network Security Groups (NSGs)
- Enable Azure Firewall for traffic inspection
- Disable public network access

### 3. Identity & Access
- Enable Multi-Factor Authentication (MFA)
- Use Azure AD with Conditional Access
- Implement Privileged Identity Management (PIM)
- Follow least privilege principle

### 4. Data Protection
- Enable encryption at rest with customer-managed keys
- Use TLS 1.3 for data in transit
- Implement data classification
- Enable soft delete and purge protection

### 5. Monitoring & Logging
- Enable diagnostic settings for all resources
- Send logs to Log Analytics workspace
- Configure Azure Sentinel for security monitoring
- Set up alerts for suspicious activities

### 6. Compliance
- Enable Azure Policy for compliance enforcement
- Regular compliance audits
- Maintain audit trails
- Document security controls

## Security Scanning

This project uses automated security scanning:

- **Checkov**: Infrastructure as Code security scanning
- **TFSec**: Terraform security scanner
- **Trivy**: Vulnerability scanning
- **Dependabot**: Dependency vulnerability alerts

All pull requests must pass security scans before merging.

## Known Security Considerations

### Azure OpenAI
- Deployed with private endpoints only
- No public network access
- Managed identity for authentication
- API keys stored in Key Vault

### Azure Machine Learning
- Managed VNet isolation
- No public IP addresses
- Private endpoints for all connections
- System-assigned managed identity

### Storage Accounts
- Public network access disabled
- Private endpoints for blob and DFS
- Customer-managed encryption keys
- Soft delete enabled

### Key Vault
- Premium SKU with HSM for sensitive keys
- Purge protection enabled
- Soft delete enabled (90 days)
- Network ACLs restrict access

## Compliance Frameworks

This project helps meet requirements for:

- **PCI-DSS v4.0**: Payment Card Industry Data Security Standard
- **HIPAA**: Health Insurance Portability and Accountability Act
- **SOC 2 Type II**: Service Organization Control 2
- **GDPR**: General Data Protection Regulation
- **CCPA**: California Consumer Privacy Act

## Security Contacts

For security-related questions or concerns:

- **Security Team**: [security@example.com]
- **Project Maintainers**: [maintainers@example.com]

## Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities. Contributors who report valid security issues will be acknowledged in our security advisories (unless they prefer to remain anonymous).

---

**Last Updated**: December 2025  
**Version**: 1.0.0
