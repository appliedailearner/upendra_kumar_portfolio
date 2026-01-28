# APIM Semantic Caching Policy (XML)
# This policy should be added to the APIM inbound/outbound sections

## Inbound Policy
```xml
<policies>
    <inbound>
        <base />
        <!-- Cache lookup using prompt as key -->
        <cache-lookup vary-by-developer="false" vary-by-developer-groups="false" caching-type="external">
            <vary-by-header>Authorization</vary-by-header>
            <vary-by-query-parameter>prompt</vary-by-query-parameter>
            <vary-by-query-parameter>max_tokens</vary-by-query-parameter>
        </cache-lookup>
        
        <!-- Rate limiting per environment -->
        <rate-limit-by-key calls="100" renewal-period="60" counter-key="@(context.Request.Headers.GetValueOrDefault("X-Environment","prod"))" />
    </inbound>
    
    <backend>
        <base />
    </backend>
    
    <outbound>
        <base />
        <!-- Store response in Redis cache for 1 hour -->
        <cache-store duration="3600" caching-type="external" />
    </outbound>
    
    <on-error>
        <base />
    </on-error>
</policies>
```

## APIM Named Values (Connection to Redis)
- **redis-connection-string**: Retrieved from Key Vault
- **cache-duration**: 3600 seconds (1 hour)

## Environment-Based Routing
```xml
<choose>
    <when condition="@(context.Request.Headers.GetValueOrDefault("X-Environment","prod") == "prod")">
        <set-backend-service base-url="https://ukl-openai-prod.openai.azure.com/openai/deployments/gpt4-prod-deployment" />
    </when>
    <when condition="@(context.Request.Headers.GetValueOrDefault("X-Environment","") == "test")">
        <set-backend-service base-url="https://ukl-openai-prod.openai.azure.com/openai/deployments/gpt4-test-deployment" />
    </when>
    <when condition="@(context.Request.Headers.GetValueOrDefault("X-Environment","") == "dev")">
        <set-backend-service base-url="https://ukl-openai-prod.openai.azure.com/openai/deployments/gpt4-dev-deployment" />
    </when>
    <otherwise>
        <return-response>
            <set-status code="400" reason="Bad Request" />
            <set-body>Invalid X-Environment header. Must be: prod, test, or dev</set-body>
        </return-response>
    </otherwise>
</choose>
```
