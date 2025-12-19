# Contributing to Azure Landing Zones Project

Thank you for your interest in contributing to the Azure Landing Zones Project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Documentation Guidelines](#documentation-guidelines)

## 📜 Code of Conduct

This project adheres to the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). By participating, you are expected to uphold this code.

## 🤝 How to Contribute

### Reporting Issues

- Use the appropriate [issue template](.github/ISSUE_TEMPLATE/)
- Include environment details (Terraform version, Azure region, etc.)
- Provide clear reproduction steps
- Include relevant logs and error messages

### Suggesting Enhancements

- Check if the enhancement has already been suggested
- Provide a clear use case and rationale
- Include examples of how it would work
- Consider backward compatibility

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/your-feature`)
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit your changes** with clear messages
7. **Push to your fork** (`git push origin feature/your-feature`)
8. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites

- Terraform >= 1.6.0
- Azure CLI >= 2.50.0
- Go >= 1.21 (for Terratest)
- Git
- Code editor (VS Code recommended)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/appliedailearner/azure-landing-zones-project.git
cd azure-landing-zones-project

# Install pre-commit hooks
pre-commit install

# Validate Terraform
cd terraform/modules/ai-landing-zone
terraform init
terraform validate
terraform fmt -check

# Run tests
cd ../../../tests/unit/terraform
go test -v
```

### Required Tools

- **Terraform**: Infrastructure as Code
- **Checkov**: Security scanning
- **TFSec**: Terraform security scanner
- **Infracost**: Cost estimation
- **Terratest**: Testing framework

## 📝 Coding Standards

### Terraform

#### Formatting
```bash
# Format all Terraform files
terraform fmt -recursive
```

#### Naming Conventions
- **Resources**: Use descriptive names with environment prefix
  ```hcl
  resource "azurerm_resource_group" "ai_lz" {
    name = "rg-${var.environment}-${var.location_short}-ai-01"
  }
  ```

- **Variables**: Use snake_case
  ```hcl
  variable "resource_group_name" {
    description = "Name of the resource group"
    type        = string
  }
  ```

- **Outputs**: Use snake_case with descriptive names
  ```hcl
  output "ml_workspace_id" {
    description = "ID of the Azure ML workspace"
    value       = azurerm_machine_learning_workspace.ml_workspace.id
  }
  ```

#### Best Practices

1. **Use Variables**: Never hardcode values
   ```hcl
   # ❌ Bad
   location = "eastus2"
   
   # ✅ Good
   location = var.location
   ```

2. **Add Validation**: Validate variable inputs
   ```hcl
   variable "environment" {
     type = string
     validation {
       condition     = contains(["dev", "staging", "prod"], var.environment)
       error_message = "Environment must be dev, staging, or prod"
     }
   }
   ```

3. **Use Descriptions**: Document all variables and outputs
   ```hcl
   variable "vnet_address_space" {
     description = "Address space for the AI Landing Zone VNet"
     type        = list(string)
   }
   ```

4. **Follow AVM Patterns**: Align with [Azure Verified Modules](https://aka.ms/AVM)

### Documentation

#### Markdown Files

- Use proper heading hierarchy (H1 → H2 → H3)
- Keep line length < 120 characters
- Include table of contents for long documents
- Use code blocks with language specification
- Add mermaid diagrams for architecture

#### Code Comments

```hcl
# Create virtual network for AI Landing Zone
# This VNet will host ML workspace, storage, and compute resources
resource "azurerm_virtual_network" "ai_vnet" {
  name                = "vnet-${var.environment}-${var.location_short}-ai-spoke"
  location            = azurerm_resource_group.ai_lz.location
  resource_group_name = azurerm_resource_group.ai_lz.name
  address_space       = var.vnet_address_space
  tags                = var.tags
}
```

## 🧪 Testing Requirements

### Unit Tests

All Terraform modules must have Terratest coverage:

```go
// tests/unit/terraform/ai_landing_zone_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestAILandingZone(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../../../terraform/modules/ai-landing-zone",
        Vars: map[string]interface{}{
            "resource_group_name": "rg-test-eus2-ai-01",
            "location":            "eastus2",
            "environment":         "dev",
            "vnet_address_space":  []string{"10.100.0.0/16"},
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // Validate outputs
    mlWorkspaceId := terraform.Output(t, terraformOptions, "ml_workspace_id")
    assert.NotEmpty(t, mlWorkspaceId)
}
```

### Security Scans

All code must pass security scans:

```bash
# Run Checkov
checkov -d terraform/

# Run TFSec
tfsec terraform/

# Run Trivy
trivy config terraform/
```

### Cost Validation

Ensure cost estimates are within budget:

```bash
# Generate cost estimate
infracost breakdown --path=terraform/modules/ai-landing-zone
```

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows our coding standards
- [ ] All tests pass locally
- [ ] Security scans pass (Checkov, TFSec)
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

### PR Template

When creating a PR, include:

1. **Description**: What does this PR do?
2. **Motivation**: Why is this change needed?
3. **Testing**: How was this tested?
4. **Screenshots**: If applicable
5. **Breaking Changes**: Any breaking changes?
6. **Checklist**: Complete the PR checklist

### Review Process

1. **Automated Checks**: CI/CD pipeline must pass
2. **Peer Review**: At least one approval required
3. **Security Review**: For security-related changes
4. **Architecture Review**: For major architectural changes

### Merge Criteria

- ✅ All CI/CD checks pass
- ✅ At least one approval
- ✅ No unresolved comments
- ✅ Branch is up to date
- ✅ Squash and merge (preferred)

## 📚 Documentation Guidelines

### Module Documentation

Each Terraform module must have:

1. **README.md**: Overview, usage, examples
2. **variables.tf**: All input variables
3. **outputs.tf**: All output values
4. **versions.tf**: Provider requirements
5. **examples/**: Working examples

### Architecture Documentation

For new components:

1. **Design Decisions**: Why this approach?
2. **Assumptions**: What are we assuming?
3. **Bill of Materials**: What resources?
4. **Detailed Design**: How does it work?
5. **Low-Level Design**: Implementation details
6. **Handover Document**: Operations guide

### Diagrams

Use Mermaid for diagrams:

```markdown
\`\`\`mermaid
graph LR
    A[User] --> B[Azure AD]
    B --> C[ML Workspace]
    C --> D[Azure OpenAI]
\`\`\`
```

## 🏷️ Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(ai-landing-zone): add Azure OpenAI deployment

- Added Azure OpenAI service with private endpoints
- Configured GPT-4 and GPT-3.5 deployments
- Updated documentation

Closes #123
```

## 🐛 Bug Reports

Use the bug report template and include:

- **Environment**: Terraform version, Azure region
- **Steps to Reproduce**: Clear steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Logs**: Relevant error messages
- **Screenshots**: If applicable

## 💡 Feature Requests

Use the feature request template and include:

- **Problem**: What problem does this solve?
- **Solution**: Proposed solution
- **Alternatives**: Other options considered
- **Use Case**: Real-world scenario
- **Impact**: Who benefits?

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Documentation**: Check the docs first

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Questions?** Open a [discussion](https://github.com/appliedailearner/azure-landing-zones-project/discussions) or create an [issue](https://github.com/appliedailearner/azure-landing-zones-project/issues).
