# Azure Storage - Fix Folder Structure

## Problem Identified

All files were uploaded to the **root** of the `$web` container, but the website expects them in specific folders.

**Current Structure (WRONG):**
```
$web/
├── index.html
├── style.css          ❌ Should be in css/
├── main.js            ❌ Should be in js/
├── profile.jpg        ❌ Should be in images/
├── operating-model.html  ❌ Should be in pages/
└── ... (all other files at root)
```

**Required Structure (CORRECT):**
```
$web/
├── index.html         ✅ Stays at root
├── CNAME             ✅ Stays at root
├── css/
│   ├── style.css     ✅ Move here
│   └── ... (all CSS files)
├── js/
│   └── main.js       ✅ Move here
├── images/
│   └── ... (all image files)
├── assets/
│   └── ... (all asset files)
├── pages/
│   ├── operating-model.html  ✅ Move here
│   ├── projects.html
│   ├── case-studies/
│   │   └── genai-rag.html
│   └── ... (all page HTML files)
└── presentations/
    └── ... (all presentation files)
```

---

## How to Fix in Azure Portal

### Step 1: Create Folders

1. Go to: Azure Portal → Storage Account → `portfolioupendrakumar` → Containers → `$web`
2. Click "Upload" → "Advanced"
3. Check "Upload to a folder"
4. Type folder name: `css`
5. Select a dummy file (any file) and upload
6. Repeat to create folders: `js`, `images`, `assets`, `pages`, `presentations`

### Step 2: Move Files to Correct Folders

Unfortunately, Azure Portal doesn't have a "move" function. You need to:

**Option A: Delete and Re-upload with Folder Structure**
1. Delete all files currently in the root (except `index.html`, `CNAME`, and `.md` files)
2. Re-upload using "Upload to folder" option:
   - Upload all CSS files → folder: `css`
   - Upload all JS files → folder: `js`
   - Upload all images → folder: `images`
   - Upload all assets → folder: `assets`
   - Upload all page HTML files → folder: `pages`
   - Upload all presentations → folder: `presentations`

**Option B: Use Azure Storage Explorer (RECOMMENDED - Much Faster)**
1. Download Azure Storage Explorer: https://azure.microsoft.com/products/storage/storage-explorer/
2. Sign in and navigate to: `portfolioupendrakumar` → Blob Containers → `$web`
3. You can drag and drop folders directly:
   - Drag `c:\MyResumePortfolio\css` folder → Drop into `$web`
   - Drag `c:\MyResumePortfolio\js` folder → Drop into `$web`
   - Drag `c:\MyResumePortfolio\images` folder → Drop into `$web`
   - Drag `c:\MyResumePortfolio\assets` folder → Drop into `$web`
   - Drag `c:\MyResumePortfolio\pages` folder → Drop into `$web`
   - Drag `c:\MyResumePortfolio\presentations` folder → Drop into `$web`
4. Delete the duplicate files from the root

---

## Quick Fix Using Azure Storage Explorer

**This is the FASTEST method:**

1. **Download and Install**
   - https://azure.microsoft.com/products/storage/storage-explorer/

2. **Connect**
   - Open Azure Storage Explorer
   - Sign in with your Azure account
   - Navigate to: Storage Accounts → portfolioupendrakumar → Blob Containers → $web

3. **Upload Folders (Preserves Structure)**
   - Click "Upload" → "Upload Folder"
   - Browse to: `c:\MyResumePortfolio\css`
   - Click "Select Folder"
   - Repeat for: js, images, assets, pages, presentations

4. **Clean Up**
   - Delete duplicate files from root (keep only index.html, CNAME, and .md files)

5. **Verify**
   - You should see folders in $web container:
     - css/ (with files inside)
     - js/ (with files inside)
     - images/ (with files inside)
     - assets/ (with files inside)
     - pages/ (with files inside)
     - presentations/ (with files inside)

---

## After Fix - Test

Visit: https://porfolioupendrakumar.z29.web.core.windows.net

**Should see:**
- ✅ Proper styling (CSS loaded)
- ✅ Images displaying
- ✅ Navigation working
- ✅ No 404 errors in console

---

## Why This Happened

When you uploaded files in Azure Portal, if you didn't check "Upload to folder" and specify the folder name, all files went to the root. The website's HTML references files with paths like `/css/style.css`, so they must be in those folders.

---

## Estimated Time to Fix

- **Azure Storage Explorer**: 5-10 minutes
- **Azure Portal (manual)**: 20-30 minutes

**Recommendation**: Use Azure Storage Explorer for the quickest fix!
