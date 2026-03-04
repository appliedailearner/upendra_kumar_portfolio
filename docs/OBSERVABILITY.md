# Portfolio Observability Governance

This document outlines the observability architecture and privacy governance for the Upendra Kumar Portfolio.

## 🛠️ Technology Stack
- **Engine**: Azure App Insights (RUM SDK)
- **Governance Layer**: `js/observability.js`
- **Privacy Controls**: Custom URL-based kill-switch and PII sanitization.

## 🛡️ Privacy Governance

### 1. Global Kill-Switch
To immediately disable all telemetry for a session (e.g., for security audits), append `?noai=1` to any URL on the site.
- **Verification**: Check the browser console for `[Telemetry] Governance: Tracking disabled via kill-switch.`

### 2. PII Sanitization
The system automatically scrubs the following from telemetry before it leaves the browser:
- **Query Parameters**: All `?` parameters in the URL and Referrer are removed to prevent sensitive data leakage.
- **IP Address**: Handled natively by Azure App Insights (masked/obfuscated depending on resource configuration).

## 📊 tracked High-Value Signals

The following custom events are tracked to measure architectural authority and engagement:

| Event Name | Description | Trigger |
|------------|-------------|---------|
| `ResumeDownload` | Executive Brief (Resume) download | Clicking the Resume button |
| `ExternalNavigation` | Interaction with authority links (LinkedIn, Medium, etc.) | Clicking external footer/social links |
| `SystemHealthCheck` | Verify site availability via `/status.json` | Background polling (automated) |

## 🧪 Testing & Validation

### Verification of Implementation
1. Open DevTools (F12) -> Console.
2. Filter for `[Telemetry]`.
3. You should see `[Telemetry] Initalized` on page load.
4. Click the Resume button; you should see `[Telemetry] Logging event: ResumeDownload`.

## 🔄 Maintenance
To update the connection string or modify sampling rates, edit `js/observability.js`. Standard sampling is set to **100%** for low-traffic authority tracking.
