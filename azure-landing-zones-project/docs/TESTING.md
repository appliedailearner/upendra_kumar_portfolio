# Testing Guide

This guide explains how to test the Azure Landing Zones Terraform modules.

## Prerequisites

- Go >= 1.21
- Terraform >= 1.6.0
- Azure CLI >= 2.50.0
- Azure subscription with appropriate permissions

## Setup

1. **Install Go dependencies**:
```bash
cd tests
go mod download
```

2. **Configure Azure credentials**:
```bash
az login
az account set --subscription <subscription-id>
```

3. **Set environment variables**:
```bash
export ARM_SUBSCRIPTION_ID="<subscription-id>"
export ARM_TENANT_ID="<tenant-id>"
export ARM_CLIENT_ID="<client-id>"
export ARM_CLIENT_SECRET="<client-secret>"
```

## Running Tests

### Run all tests:
```bash
cd tests/unit/terraform
go test -v -timeout 60m
```

### Run specific test:
```bash
go test -v -timeout 60m -run TestAILandingZoneBasic
```

### Run tests in parallel:
```bash
go test -v -timeout 60m -parallel 4
```

## Test Structure

```
tests/
├── unit/
│   └── terraform/
│       └── ai_landing_zone_test.go
├── integration/
│   └── (future integration tests)
└── go.mod
```

## Writing Tests

Example test structure:

```go
func TestMyFeature(t *testing.T) {
    t.Parallel()
    
    terraformOptions := &terraform.Options{
        TerraformDir: "../../../terraform/modules/ai-landing-zone",
        Vars: map[string]interface{}{
            "resource_group_name": "rg-test",
            // ... other variables
        },
    }
    
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)
    
    // Assertions
    output := terraform.Output(t, terraformOptions, "output_name")
    assert.NotEmpty(t, output)
}
```

## Cleanup

Tests automatically clean up resources using `defer terraform.Destroy()`.

For manual cleanup:
```bash
cd terraform/modules/ai-landing-zone
terraform destroy
```
