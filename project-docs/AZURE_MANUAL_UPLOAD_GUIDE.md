# Azure Storage - Manual Folder Upload Guide

Since the Azure CLI cannot access the storage account (likely due to subscription permissions), here's how to complete the upload manually through the Azure Portal.

## Quick Upload Instructions

### Method 1: Azure Portal (Recommended)

1. **Open Azure Portal**
   - Go to: https://portal.azure.com
   - Navigate to: Storage Account → `portfolioupendrakumar` → Containers → `$web`

2. **Upload CSS Folder**
   - Click "Upload" button
   - Click "Advanced" to expand options
   - Check "Upload to a folder"
   - Enter folder name: `css`
   - Click "Browse for files"
   - Navigate to: `c:\MyResumePortfolio\css`
   - Select ALL files in the css folder
   - Click "Upload"

3. **Upload JS Folder**
   - Click "Upload" button again
   - Click "Advanced"
   - Check "Upload to a folder"
   - Enter folder name: `js`
   - Select all files from: `c:\MyResumePortfolio\js`
   - Click "Upload"

4. **Upload Images Folder**
   - Click "Upload" button
   - Click "Advanced"
   - Check "Upload to a folder"
   - Enter folder name: `images`
   - Select all files from: `c:\MyResumePortfolio\images`
   - Click "Upload"

5. **Upload Assets Folder**
   - Click "Upload" button
   - Click "Advanced"
   - Check "Upload to a folder"
   - Enter folder name: `assets`
   - Select all files from: `c:\MyResumePortfolio\assets`
   - Click "Upload"

6. **Upload Pages Folder**
   - Click "Upload" button
   - Click "Advanced"
   - Check "Upload to a folder"
   - Enter folder name: `pages`
   - Select all files from: `c:\MyResumePortfolio\pages`
   - Click "Upload"
   - **IMPORTANT**: Pages folder has subfolders (case-studies)
   - After uploading pages, create subfolder: `pages/case-studies`
   - Upload files from: `c:\MyResumePortfolio\pages\case-studies`

7. **Upload Presentations Folder**
   - Click "Upload" button
   - Click "Advanced"
   - Check "Upload to a folder"
   - Enter folder name: `presentations`
   - Select all files from: `c:\MyResumePortfolio\presentations`
   - Click "Upload"

---

## Method 2: Azure Storage Explorer (Faster for Multiple Folders)

If you have Azure Storage Explorer installed:

1. **Download Azure Storage Explorer** (if not installed)
   - https://azure.microsoft.com/en-us/products/storage/storage-explorer/

2. **Connect to Storage Account**
   - Open Azure Storage Explorer
   - Sign in with your Azure account
   - Navigate to: Storage Accounts → portfolioupendrakumar → Blob Containers → $web

3. **Upload Folders**
   - Right-click on `$web` container
   - Select "Upload" → "Upload Folder"
   - Browse to `c:\MyResumePortfolio\css` and upload
   - Repeat for: js, images, assets, pages, presentations

---

## Folders to Upload

| Folder | Location | Contains |
|--------|----------|----------|
| **css** | `c:\MyResumePortfolio\css` | All CSS stylesheets |
| **js** | `c:\MyResumePortfolio\js` | JavaScript files |
| **images** | `c:\MyResumePortfolio\images` | Image files |
| **assets** | `c:\MyResumePortfolio\assets` | Additional assets |
| **pages** | `c:\MyResumePortfolio\pages` | HTML sub-pages + case-studies subfolder |
| **presentations** | `c:\MyResumePortfolio\presentations` | Presentation HTML files |

---

## After Upload - Verify

1. **Check the $web container** should have:
   ```
   $web/
   ├── index.html
   ├── CNAME
   ├── css/
   │   ├── style.css
   │   └── ... (other CSS files)
   ├── js/
   │   └── main.js
   ├── images/
   │   └── ... (image files)
   ├── assets/
   │   └── ... (asset files)
   ├── pages/
   │   ├── projects.html
   │   ├── case-studies/
   │   │   └── genai-rag.html
   │   └── ... (other pages)
   └── presentations/
       └── ... (presentation files)
   ```

2. **Test the website**
   - Visit: https://porfolioupendrakumar.z29.web.core.windows.net
   - Page should now load with full styling
   - All images should display
   - Navigation should work

---

## Why Azure CLI Failed

The Azure CLI couldn't access the storage account because:
- Storage account is in a different subscription than the one currently selected
- Or requires different authentication method
- Manual upload through Azure Portal bypasses these issues

---

## Estimated Time

- **Azure Portal**: ~10-15 minutes (uploading each folder separately)
- **Azure Storage Explorer**: ~5 minutes (can upload multiple folders at once)

Choose the method that works best for you!
