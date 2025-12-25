# DNS Configuration Fix for portfolio.upendrakumar.com

## Problem Identified

Your `portfolio.upendrakumar.com` subdomain is currently showing an "Invalid URI" error because the Cloudflare DNS CNAME record is pointing to the wrong endpoint.

### Current (Incorrect) Configuration:
- **DNS CNAME**: `portfolio` → `portfolioupendrakumar.z29.web.core.windows.net`
- **Result**: Error because Azure Storage doesn't recognize this custom domain

### Required Configuration:

You need to decide which platform will serve `portfolio.upendrakumar.com`:

## Option 1: Use GitHub Pages (Recommended)

**DNS Configuration in Cloudflare:**
```
Type: CNAME
Name: portfolio
Content: appliedailearner.github.io
Proxy status: DNS only (gray cloud)
```

**Why this works:**
- GitHub Pages already has your CNAME file configured
- GitHub will automatically serve your site at portfolio.upendrakumar.com
- Free SSL/TLS through GitHub

**Steps:**
1. Go to Cloudflare DNS management for upendrakumar.com
2. Edit the "portfolio" CNAME record
3. Change content from `portfolioupendrakumar.z29.web.core.windows.net` to `appliedailearner.github.io`
4. Set Proxy status to "DNS only" (gray cloud icon)
5. Save changes
6. Wait 5-10 minutes for DNS propagation

---

## Option 2: Use Azure Storage

If you want to use Azure Storage for the custom domain instead:

**DNS Configuration in Cloudflare:**
```
Type: CNAME
Name: asverify.portfolio
Content: asverify.portfolioupendrakumar.z29.web.core.windows.net

Type: CNAME
Name: portfolio
Content: portfolioupendrakumar.z29.web.core.windows.net
Proxy status: DNS only (gray cloud)
```

**Additional Azure Configuration Required:**
1. In Azure Portal, go to your storage account
2. Navigate to: Static website → Custom domain
3. Add custom domain: `portfolio.upendrakumar.com`
4. Enable HTTPS (requires Azure CDN for custom domain SSL)

**Note:** This option is more complex and may require Azure CDN for SSL support.

---

## Recommended Deployment Strategy

Based on your setup, here's the recommended approach:

### Primary Domain Setup:
- **portfolio.upendrakumar.com** → GitHub Pages (free, easy SSL)
- **portfolioupendrakumar.z29.web.core.windows.net** → Azure Storage (backup/testing)

### Benefits:
1. ✅ Free SSL certificate from GitHub
2. ✅ Automatic deployments via GitHub Actions
3. ✅ Azure Storage as backup/alternative endpoint
4. ✅ Easy to manage and update

---

## Quick Fix (5 Minutes)

**To fix the error immediately:**

1. **Open Cloudflare Dashboard**
   - Go to: https://dash.cloudflare.com
   - Select domain: `upendrakumar.com`
   - Click "DNS" in the left menu

2. **Edit the portfolio CNAME record**
   - Find the record: `portfolio` → `portfolioupendrakumar.z29.web.core.windows.net`
   - Click "Edit"
   - Change "Content" to: `appliedailearner.github.io`
   - Set "Proxy status" to "DNS only" (click the orange cloud to make it gray)
   - Click "Save"

3. **Verify in GitHub**
   - Go to: https://github.com/appliedailearner/upendra_kumar_portfolio/settings/pages
   - Confirm custom domain shows: `portfolio.upendrakumar.com`
   - Wait for DNS check to complete (green checkmark)

4. **Test**
   - Wait 5-10 minutes for DNS propagation
   - Visit: https://portfolio.upendrakumar.com
   - Should load your portfolio website

---

## Both Endpoints Working

After the fix, you'll have:

| Endpoint | URL | Purpose |
|----------|-----|---------|
| **GitHub Pages** | https://portfolio.upendrakumar.com | Primary production site |
| **GitHub Pages** | https://appliedailearner.github.io/upendra_kumar_portfolio | Direct GitHub URL |
| **Azure Storage** | https://portfolioupendrakumar.z29.web.core.windows.net | Backup/testing endpoint |

You can deploy to both using the scripts I'll create next!
