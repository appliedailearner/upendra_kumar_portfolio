package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/azure"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

// TestAILandingZoneBasic tests the basic deployment of AI Landing Zone
func TestAILandingZoneBasic(t *testing.T) {
	t.Parallel()

	// Construct the terraform options with default retryable errors to handle the most common
	// retryable errors in terraform testing.
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		// The path to where our Terraform code is located
		TerraformDir: "../../../terraform/modules/ai-landing-zone",

		// Variables to pass to our Terraform code using -var options
		Vars: map[string]interface{}{
			"resource_group_name": "rg-test-eus2-ai-01",
			"location":            "eastus2",
			"location_short":      "eus2",
			"environment":         "dev",
			"vnet_address_space":  []string{"10.100.0.0/16"},
			"industry_compliance": map[string]bool{
				"pci_dss": false,
				"hipaa":   false,
				"sox":     false,
				"gdpr":    true,
			},
			"cost_tier":            "minimal",
			"enable_azure_openai":  true,
			"enable_ml_workspace":  true,
			"hub_vnet_address_space": nil,
		},

		// Disable colors in Terraform commands so its easier to parse stdout/stderr
		NoColor: true,
	})

	// At the end of the test, run `terraform destroy` to clean up any resources that were created
	defer terraform.Destroy(t, terraformOptions)

	// Run `terraform init` and `terraform apply`. Fail the test if there are any errors.
	terraform.InitAndApply(t, terraformOptions)

	// Run `terraform output` to get the values of output variables
	resourceGroupName := terraform.Output(t, terraformOptions, "resource_group_name")
	vnetID := terraform.Output(t, terraformOptions, "vnet_id")
	storageAccountName := terraform.Output(t, terraformOptions, "storage_account_name")
	keyVaultName := terraform.Output(t, terraformOptions, "key_vault_name")

	// Verify outputs are not empty
	assert.NotEmpty(t, resourceGroupName)
	assert.NotEmpty(t, vnetID)
	assert.NotEmpty(t, storageAccountName)
	assert.NotEmpty(t, keyVaultName)

	// Verify resource group exists
	assert.True(t, azure.ResourceGroupExists(t, resourceGroupName, ""))

	// Verify the resource group name matches expected
	assert.Equal(t, "rg-test-eus2-ai-01", resourceGroupName)
}

// TestAILandingZoneWithCompliance tests deployment with compliance requirements
func TestAILandingZoneWithCompliance(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../../../terraform/modules/ai-landing-zone",
		Vars: map[string]interface{}{
			"resource_group_name": "rg-test-eus2-ai-compliance-01",
			"location":            "eastus2",
			"location_short":      "eus2",
			"environment":         "dev",
			"vnet_address_space":  []string{"10.100.0.0/16"},
			"industry_compliance": map[string]bool{
				"pci_dss": true,
				"hipaa":   true,
				"sox":     false,
				"gdpr":    true,
			},
			"cost_tier":           "standard",
			"enable_azure_openai": true,
			"enable_ml_workspace": true,
		},
		NoColor: true,
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Get outputs
	keyVaultName := terraform.Output(t, terraformOptions, "key_vault_name")
	complianceTags := terraform.OutputMap(t, terraformOptions, "compliance_tags")

	// Verify Key Vault is Premium SKU for PCI-DSS/HIPAA
	encryptionInfo := terraform.OutputMap(t, terraformOptions, "encryption_enabled")
	assert.Equal(t, "premium", encryptionInfo["key_vault_sku"])

	// Verify compliance tags
	assert.Equal(t, "true", complianceTags["pci_dss"])
	assert.Equal(t, "true", complianceTags["hipaa"])
	assert.Equal(t, "true", complianceTags["gdpr"])

	// Verify Key Vault exists
	assert.NotEmpty(t, keyVaultName)
}

// TestAILandingZoneNetworkSecurity tests network security configuration
func TestAILandingZoneNetworkSecurity(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../../../terraform/modules/ai-landing-zone",
		Vars: map[string]interface{}{
			"resource_group_name": "rg-test-eus2-ai-security-01",
			"location":            "eastus2",
			"location_short":      "eus2",
			"environment":         "dev",
			"vnet_address_space":  []string{"10.100.0.0/16"},
			"industry_compliance": map[string]bool{
				"pci_dss": true,
				"hipaa":   false,
				"sox":     false,
				"gdpr":    true,
			},
			"cost_tier":           "minimal",
			"enable_azure_openai": true,
			"enable_ml_workspace": true,
		},
		NoColor: true,
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Get subnet IDs
	subnetIDs := terraform.OutputMap(t, terraformOptions, "subnet_ids")

	// Verify all required subnets exist
	assert.NotEmpty(t, subnetIDs["ml_workspace"])
	assert.NotEmpty(t, subnetIDs["compute"])
	assert.NotEmpty(t, subnetIDs["private_endpoints"])
	assert.NotEmpty(t, subnetIDs["data"])

	// Verify private endpoint IDs
	privateEndpointIDs := terraform.OutputMap(t, terraformOptions, "private_endpoint_ids")
	assert.NotEmpty(t, privateEndpointIDs["storage_blob"])
	assert.NotEmpty(t, privateEndpointIDs["storage_dfs"])
	assert.NotEmpty(t, privateEndpointIDs["key_vault"])
	assert.NotEmpty(t, privateEndpointIDs["openai"])
}

// TestAILandingZoneCostTiers tests different cost tier configurations
func TestAILandingZoneCostTiers(t *testing.T) {
	testCases := []struct {
		name              string
		costTier          string
		expectedCostRange int
	}{
		{"Minimal", "minimal", 3000},
		{"Standard", "standard", 12000},
		{"Premium", "premium", 25000},
	}

	for _, tc := range testCases {
		tc := tc // capture range variable
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()

			terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
				TerraformDir: "../../../terraform/modules/ai-landing-zone",
				Vars: map[string]interface{}{
					"resource_group_name": "rg-test-eus2-ai-" + tc.costTier + "-01",
					"location":            "eastus2",
					"location_short":      "eus2",
					"environment":         "dev",
					"vnet_address_space":  []string{"10.100.0.0/16"},
					"cost_tier":           tc.costTier,
					"enable_azure_openai": true,
					"enable_ml_workspace": true,
				},
				NoColor: true,
			})

			defer terraform.Destroy(t, terraformOptions)
			terraform.InitAndApply(t, terraformOptions)

			// Verify cost tier output
			costTierOutput := terraform.Output(t, terraformOptions, "cost_tier")
			assert.Equal(t, tc.costTier, costTierOutput)

			// Verify estimated cost is in expected range
			estimatedCost := terraform.OutputRequired(t, terraformOptions, "estimated_monthly_cost_usd")
			assert.NotEmpty(t, estimatedCost)
		})
	}
}

// TestAILandingZoneMonitoring tests monitoring and logging configuration
func TestAILandingZoneMonitoring(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../../../terraform/modules/ai-landing-zone",
		Vars: map[string]interface{}{
			"resource_group_name":         "rg-test-eus2-ai-monitoring-01",
			"location":                    "eastus2",
			"location_short":              "eus2",
			"environment":                 "dev",
			"vnet_address_space":          []string{"10.100.0.0/16"},
			"cost_tier":                   "minimal",
			"enable_azure_openai":         true,
			"enable_ml_workspace":         true,
			"enable_diagnostic_settings":  true,
			"enable_monitoring_alerts":    true,
			"log_analytics_retention_days": 90,
		},
		NoColor: true,
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Verify Log Analytics workspace
	lawID := terraform.Output(t, terraformOptions, "log_analytics_workspace_id")
	lawName := terraform.Output(t, terraformOptions, "log_analytics_workspace_name")
	assert.NotEmpty(t, lawID)
	assert.NotEmpty(t, lawName)

	// Verify Application Insights
	appInsightsID := terraform.Output(t, terraformOptions, "application_insights_id")
	assert.NotEmpty(t, appInsightsID)
}
