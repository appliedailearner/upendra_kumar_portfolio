# Portfolio Website Deployment Guide

Complete guide for deploying your portfolio website to GitHub Pages and Azure Storage Account.

---

## 🚨 IMMEDIATE FIX REQUIRED

Your `portfolio.upendrakumar.com` is currently showing an error because the DNS is misconfigured.

**Quick Fix (5 minutes):**

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → `upendrakumar.com` → DNS
2. Find the CNAME record: `portfolio` → `portfolioupendrakumar.z29.web.core.windows.net`
3. Click "Edit" and change:
   - **Content**: `appliedailearner.github.io`
   - **Proxy status**: DNS only (gray cloud)
4. Save and wait 5-10 minutes

**See [DNS_FIX_GUIDE.md](./DNS_FIX_GUIDE.md) for detailed explanation.**

---

## 📋 Prerequisites

### For GitHub Pages (Already Set Up ✓)
- ✅ Repository: `appliedailearner/upendra_kumar_portfolio`
- ✅ CNAME file configured
- ✅ Custom domain: `portfolio.upendrakumar.com`

### For Azure Storage
- ✅ Storage Account: `portfolioupendrakumar`
- ✅ Static website enabled
- ⚠️ Azure CLI required (see installation below)

### Install Azure CLI (if not installed)

**Windows:**
```powershell
# Download and run installer
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
```

**Or download from:** https://aka.ms/installazurecliwindows

**After installation:**
```powershell
# Login to Azure
az login
```

---

## 🚀 Deployment Options

### Option 1: Deploy to GitHub Pages Only

**Automatic (Recommended):**
```bash
# Just push to GitHub - GitHub Actions will deploy automatically
git add .
git commit -m "Update portfolio"
git push origin main
```

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically deploy your site.

**Manual:**
- GitHub Pages deploys automatically from the `main` branch
- No manual steps needed!

---

### Option 2: Deploy to Azure Storage Only

```powershell
# Run the Azure deployment script
.\deploy-azure.ps1
```

This script will:
- ✓ Check Azure CLI installation
- ✓ Verify you're logged in
- ✓ Upload all website files to Azure Storage
- ✓ Show deployment progress

---

### Option 3: Deploy to Both (Recommended)

```powershell
# Deploy to both GitHub Pages and Azure Storage
.\deploy-both.ps1
```

Or with a custom commit message:
```powershell
.\deploy-both.ps1 -CommitMessage "Updated case studies and presentations"
```

This script will:
1. Commit and push to GitHub (triggers GitHub Actions)
2. Deploy to Azure Storage
3. Show both deployment URLs

---

## 🌐 Your Website URLs

After deployment, your website will be available at:

| Platform | URL | Status |
|----------|-----|--------|
| **GitHub Pages (Primary)** | https://portfolio.upendrakumar.com | Custom domain |
| **GitHub Pages (Direct)** | https://appliedailearner.github.io/upendra_kumar_portfolio | Direct URL |
| **Azure Storage** | https://portfolioupendrakumar.z29.web.core.windows.net | Backup endpoint |

---

## 📝 Deployment Workflow

### Daily Development Workflow

1. **Make changes** to your website files
2. **Test locally** (open `index.html` in browser)
3. **Deploy**:
   ```powershell
   .\deploy-both.ps1 -CommitMessage "Your change description"
   ```
4. **Verify** at both URLs

### GitHub Actions Workflow

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:
- Triggers on every push to `main` branch
- Can be manually triggered from GitHub Actions tab
- Deploys to GitHub Pages
- Takes ~2-3 minutes to complete

**To manually trigger:**
1. Go to: https://github.com/appliedailearner/upendra_kumar_portfolio/actions
2. Click "Deploy to GitHub Pages"
3. Click "Run workflow"

---

## 🔧 Troubleshooting

### GitHub Pages Issues

**Problem:** Changes not showing up
```bash
# Check GitHub Actions status
# Go to: https://github.com/appliedailearner/upendra_kumar_portfolio/actions

# Force clear cache
# Add ?v=timestamp to URL, e.g., https://portfolio.upendrakumar.com?v=123
```

**Problem:** Custom domain not working
- Check DNS settings in Cloudflare (see DNS_FIX_GUIDE.md)
- Verify CNAME file contains: `portfolio.upendrakumar.com`
- Check GitHub Pages settings: Settings → Pages → Custom domain

### Azure Storage Issues

**Problem:** "Azure CLI not found"
```powershell
# Install Azure CLI
winget install Microsoft.AzureCLI
# Or download from: https://aka.ms/installazurecliwindows
```

**Problem:** "Not logged in to Azure"
```powershell
az login
```

**Problem:** "Access denied"
```powershell
# Check your subscription
az account show

# List available subscriptions
az account list --output table

# Set the correct subscription
az account set --subscription "Visual Studio Enterprise Subscription"
```

### DNS Issues

**Problem:** "Invalid URI" error on portfolio.upendrakumar.com

See **[DNS_FIX_GUIDE.md](./DNS_FIX_GUIDE.md)** for complete solution.

---

## 🎯 Best Practices

1. **Always test locally** before deploying
2. **Use meaningful commit messages** for better tracking
3. **Deploy to both platforms** for redundancy
4. **Monitor GitHub Actions** for deployment status
5. **Keep CNAME file** in repository root

---

## 📂 Files Overview

| File | Purpose |
|------|---------|
| `.github/workflows/deploy.yml` | GitHub Actions workflow for automatic deployment |
| `deploy-azure.ps1` | PowerShell script for Azure Storage deployment |
| `deploy-both.ps1` | Unified script for deploying to both platforms |
| `CNAME` | Custom domain configuration for GitHub Pages |
| `DNS_FIX_GUIDE.md` | Detailed DNS configuration guide |

---

## 🔐 Security Notes

- Azure CLI credentials are stored securely by Azure
- GitHub Actions uses repository secrets (no credentials in code)
- Both platforms provide free SSL/TLS certificates
- Keep your Azure credentials private

---

## 📞 Quick Reference

**Deploy to both platforms:**
```powershell
.\deploy-both.ps1
```

**Deploy to Azure only:**
```powershell
.\deploy-azure.ps1
```

**Deploy to GitHub only:**
```bash
git push origin main
```

**Check deployment status:**
- GitHub: https://github.com/appliedailearner/upendra_kumar_portfolio/actions
- Azure: https://portal.azure.com → portfolioupendrakumar → Static website

---

## ✅ Next Steps

1. **Fix DNS** (see top of this document)
2. **Test Azure deployment**: `.\deploy-azure.ps1`
3. **Verify both URLs** work correctly
4. **Set up regular deployment workflow**

For detailed DNS fix instructions, see **[DNS_FIX_GUIDE.md](./DNS_FIX_GUIDE.md)**.
