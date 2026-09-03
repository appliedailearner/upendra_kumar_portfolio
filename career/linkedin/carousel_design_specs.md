# LinkedIn Carousel Slide Design Specifications

**Format**: 1080x1080px (Square)  
**Tools**: Canva (recommended), PowerPoint, or Figma  
**Style**: Professional, Microsoft Azure aesthetic

---

## Design System

### Colors
- **Primary Purple**: #A855F7
- **Primary Blue**: #3B82F6
- **Dark Navy**: #0F172A
- **Success Green**: #10B981
- **Warning Yellow**: #FBBF24
- **White**: #FFFFFF
- **Text Dark**: #1E293B

### Fonts
- **Headings**: Outfit Bold or Inter Bold
- **Body**: Inter Regular or Roboto
- **Sizes**: 
  - Main Title: 72-80px
  - Subtitle: 48-56px
  - Body: 32-36px
  - Small text: 24-28px

### Gradients
- **Purple-Blue**: Linear gradient from #A855F7 to #3B82F6 (135deg)
- **Dark**: Linear gradient from #0F172A to #1E293B (135deg)

---

## Slide 1: Hook

### Layout
- **Background**: Dark gradient (#0F172A to #6366F1)
- **Alignment**: Center

### Content
```
[Large Bold Text - 80px - White]
We spent £20,000/month
on AI infrastructure.

[Medium Text - 56px - White]
Here's why the regulator
said "YES" ✅

[Small Text - 32px - Light Gray]
(And how you can too)
```

### Design Notes
- Use plenty of white space
- Checkmark emoji should be green (#10B981)
- Text should be center-aligned
- Add subtle glow effect around text

---

## Slide 2: The Problem

### Layout
- **Background**: White (#FFFFFF)
- **Accent**: Red border on left (4px, #EF4444)

### Content
```
[Red X Icon - 80px]
❌

[Title - 56px - Dark]
THE CHALLENGE

[Body - 32px - Dark Gray]
Most AI platforms fail
regulatory audits because:

[Bullet Points - 36px - Dark]
• Public endpoints
• No audit trails
• Shared capacity (PAYG)
• Zero data residency proof

[Italic Text - 32px - Gray]
Sound familiar?
```

### Design Notes
- Left-align all text
- 60px padding on all sides
- Bullet points with 40px left indent
- Red accent color for emphasis

---

## Slide 3: The Solution

### Layout
- **Background**: Purple gradient (#A855F7 to #3B82F6)
- **Alignment**: Center

### Content
```
[Green Checkmark - 80px]
✅

[Title - 56px - White]
THE SOLUTION

[Subtitle - 72px - White Bold]
The 4-Subscription
AI Fortress

[Benefits - 40px - White]
🔒 100% Private networking
🎯 PTU split (30/10/10)
⚡ Redis semantic caching
🛡️ MCSB v2 compliance
```

### Design Notes
- Center-aligned
- Each benefit on separate line
- Emojis should be 48px
- 20px spacing between benefits

---

## Slide 4: Architecture Diagram

### Layout
- **Background**: Light gray (#F8FAFC)
- **Diagram**: Simple flowchart

### Content
```
[Flowchart - Vertical]
┌─────────────────────┐
│ Azure Front Door    │
│   (Global Edge)     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Hub Firewall      │
│     (IDPS)          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Private AKS       │
│  (App Layer)        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   OpenAI PTU        │
│  (30/10/10 Split)   │
└─────────────────────┘

[Side Text - 36px]
Hub-and-Spoke Topology
4 Subscriptions
Zero Public Endpoints
```

### Design Notes
- Use blue boxes (#3B82F6) with white text
- Arrows should be thick (8px)
- Side text in purple (#A855F7)
- Clean, minimal style

---

## Slide 5: Performance

### Layout
- **Background**: Blue-purple gradient
- **Alignment**: Center

### Content
```
[Rocket Emoji - 80px]
🚀

[Title - 56px - White]
PERFORMANCE

[Large Number - 120px - Gradient Text]
72%

[Label - 40px - White]
Cache Hit Rate

[Body - 32px - White]
Redis semantic caching
saves £4,200/month in
wasted OpenAI calls

[Small Text - 28px - Light Gray]
That's 50M+ requests
answered instantly.
```

### Design Notes
- 72% should have gradient fill (purple to blue)
- Center all text
- Use bold font for number
- Add subtle shadow behind number

---

## Slide 6: Security

### Layout
- **Background**: Dark navy (#0F172A)
- **Accent**: Green highlights

### Content
```
[Shield Emoji - 80px]
🛡️

[Title - 56px - White]
SECURITY

[Large Number - 140px - Green Gradient]
0

[Label - 40px - White]
Security Incidents
in 6 months

[Bullet Points - 32px - White]
• Private Link only
• MCSB v2 (420+ controls)
• Passed 3 regulatory audits

[Bottom Text - 32px - Light Gray]
Zero-trust architecture
that actually works.
```

### Design Notes
- Zero should be bright green (#10B981)
- Add glow effect to zero
- Bullets should have green dots
- Bottom text in italics

---

## Slide 7: Reliability

### Layout
- **Background**: Blue gradient
- **Alignment**: Center

### Content
```
[Lightning Emoji - 80px]
⚡

[Title - 56px - White]
RELIABILITY

[Large Text - 80px - White Bold]
99.97% Uptime

[Comparison - 32px - Light Gray]
(vs. 95% with PAYG)

[Analogy - 36px - White]
PTU = Your private jet
PAYG = Commercial flight

[Question - 32px - Light Gray Italic]
Which would you choose
for mission-critical AI?
```

### Design Notes
- 99.97% should be extra bold
- Use airplane emojis for analogy (✈️)
- Center-aligned
- Question in italics for emphasis

---

## Slide 8: Lesson Learned

### Layout
- **Background**: Yellow-orange gradient (#FBBF24 to #F97316)
- **Alignment**: Left

### Content
```
[Warning Triangle - 80px]
⚠️

[Title - 48px - Dark]
HARD-EARNED LESSON

[Quote - 64px - Dark Bold]
"The DNS Resolver
cost us 3 days"

[Body - 32px - Dark]
We tried to skip the
Azure Private DNS Resolver.

Big mistake.

£50/month saved us from
a 3-day debugging nightmare.
```

### Design Notes
- Quote should be in quotation marks
- "Big mistake" should be bold
- Use dark text (#1E293B) for readability
- Left-align with 60px padding

---

## Slide 9: Results Summary

### Layout
- **Background**: Purple gradient
- **Grid**: 2x3 layout

### Content
```
[Chart Emoji - 80px]
📊

[Title - 56px - White]
RESULTS AFTER 6 MONTHS

[Grid - 6 Items - 36px - White]
┌──────────────┬──────────────┐
│  50M+        │  99.97%      │
│  requests/   │  uptime      │
│  month       │              │
├──────────────┼──────────────┤
│  0           │  72%         │
│  security    │  cache hit   │
│  incidents   │  rate        │
├──────────────┼──────────────┤
│  £4,200      │  3/3         │
│  monthly     │  audits      │
│  savings     │  passed      │
└──────────────┴──────────────┘

[Bottom Text - 32px - White Italic]
Real architecture.
Real results.
```

### Design Notes
- Each grid cell should have subtle border
- Numbers should be bold and larger (48px)
- Labels should be smaller (28px)
- Grid cells with light purple background (#A855F720)

---

## Slide 10: Call-to-Action

### Layout
- **Background**: White
- **Accent**: Blue elements

### Content
```
[Title - 64px - Dark Bold]
Want to build this?

[Subheading - 40px - Purple]
📥 Download the full
   Architecture Kit:

[Checklist - 36px - Dark]
✅ Terraform code
✅ Compliance matrix
✅ Cost calculator
✅ Deployment guide

[CTA - 48px - Blue]
Link in comments 👇

[Small Text - 32px - Gray]
Or DM me for a
30-min architecture review.
```

### Design Notes
- Checkmarks should be green (#10B981)
- "Link in comments" should be bold
- Down arrow should be large (56px)
- Add subtle blue border around entire slide (4px)

---

## Quick Start Guide

### Using Canva (Recommended):
1. Go to Canva.com
2. Create custom size: 1080x1080px
3. Search for "LinkedIn Carousel" templates
4. Use "Blank" template or modern tech template
5. Copy text from specifications above
6. Apply color scheme (purple/blue gradient)
7. Export as PNG (high quality)

### Using PowerPoint:
1. Create new presentation
2. Set slide size to 1080x1080px (Design → Slide Size → Custom)
3. Use gradient fills for backgrounds
4. Insert text boxes with specifications
5. Export as PNG (File → Export → PNG)

### Using Figma:
1. Create new file
2. Create frame: 1080x1080px
3. Use auto-layout for consistent spacing
4. Apply color styles from design system
5. Export as PNG (2x resolution)

---

## Pro Tips

1. **Consistency**: Use same fonts and colors across all slides
2. **White Space**: Don't overcrowd slides - less is more
3. **Contrast**: Ensure text is readable (use dark text on light backgrounds)
4. **Emojis**: Use native emojis or high-quality emoji graphics
5. **Alignment**: Keep everything aligned to grid (use guides)
6. **Export**: Export at 2x resolution for crisp images
7. **Preview**: View slides on mobile before posting

---

## Canva Template Search Terms

If using Canva templates, search for:
- "Tech startup pitch deck"
- "SaaS product carousel"
- "LinkedIn carousel modern"
- "Business metrics infographic"
- "Corporate presentation gradient"

Then customize with your content and colors.

---

## Alternative: Use Canva Magic Design

1. Go to Canva
2. Select "LinkedIn Carousel"
3. Use "Magic Design" feature
4. Paste your text content
5. Select "Tech/Corporate" style
6. Let Canva auto-generate
7. Customize colors to purple/blue

---

## Estimated Time

- **Canva (with template)**: 30-45 minutes
- **PowerPoint**: 60-90 minutes
- **Figma**: 45-60 minutes

---

## Next Steps

1. Choose your tool (Canva recommended for speed)
2. Create slides 1-10 using specifications above
3. Export as PNG files
4. Upload to LinkedIn as carousel post
5. Use caption from `linkedin_carousel_content.md`
6. Schedule for Tuesday 9 AM GMT

---

## Need Help?

If you need the slides created professionally:
- **Fiverr**: Search "LinkedIn carousel design" ($20-50)
- **Upwork**: Hire graphic designer ($50-100)
- **Canva Pro**: Use AI design features ($12.99/month)

Or wait 2h 43m for image generation quota to reset and I can create them for you!
