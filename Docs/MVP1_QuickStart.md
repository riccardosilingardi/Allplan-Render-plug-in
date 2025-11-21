# Allplan Render AI - MVP1 Quick Start Guide

## 🎉 MVP1: Basic AI Rendering

Congratulations! You have the MVP1 release which includes **basic AI rendering with Nano Banana/Nano Banana Pro**.

---

## 📦 What's Included in MVP1

### Nodes Available

1. **Load Image** - Load images from disk
2. **Save Image** - Save images with custom filenames
3. **Preview Image** - Quick preview in system viewer
4. **AI Render Basic** - Generate photorealistic renders with Nano Banana

### Features

✅ AI-powered rendering with Google Gemini
✅ Support for both Nano Banana (fast, cheap) and Nano Banana Pro (high quality)
✅ Style presets (Modern, Classical, Industrial, etc.)
✅ Lighting presets (Dawn, Noon, Sunset, Night, etc.)
✅ Multiple resolutions (1K, 2K, 4K)
✅ Automatic cost tracking
✅ Budget limits

---

## 🚀 Installation

### Step 1: Install Dependencies

```bash
python install_dependencies.py
```

This will install all required Python packages to Allplan's Python environment.

### Step 2: Configure API Keys

1. Copy `.env.template` to `.env`
2. Get your Gemini API key from: https://aistudio.google.com/app/apikey
3. Edit `.env` and add your API key:

```env
GOOGLE_GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Copy to Allplan

Copy the `VisualScripts` folder to Allplan's directory:

**Windows:**
```
C:\ProgramData\Nemetschek\Allplan\2025\Std\VisualScripts\AllplanRenderAI\
```

**Note:** Create the `AllplanRenderAI` directory if it doesn't exist.

### Step 4: Restart Allplan

Close and reopen Allplan. The custom nodes will appear in Visual Scripting.

---

## 📘 Basic Workflow Example

Here's how to create your first AI render:

### Workflow: Simple AI Rendering

```
[Load Image]
  ├─ FilePath: C:\MyProject\viewport.png
  ├─ AutoResize: True
  └─ TargetResolution: 2K
      ↓
[AI Render Basic]
  ├─ InputImagePath: (from Load Image)
  ├─ Prompt: "Modern residential building with glass facade, landscaped plaza, people walking, photorealistic"
  ├─ StylePreset: Modern
  ├─ LightingPreset: Sunset
  ├─ Resolution: 2K
  └─ UseProModel: False (use True for best quality)
      ↓
[Save Image]
  ├─ ImagePath: (from AI Render)
  ├─ OutputPath: C:\Allplan_Output\render.png
  ├─ Format: PNG
  └─ AddTimestamp: True
      ↓
[Preview Image]
  └─ ImagePath: (from Save Image)
```

---

## 🎨 Using the Nodes

### Load Image Node

**Purpose:** Load an image file to use as input for AI rendering.

**Inputs:**
- **File Path:** Click the "..." button to browse for your image
- **Auto Resize:** Enable to automatically fit the image to target resolution
- **Target Resolution:** Choose 1K, 2K, or 4K

**Outputs:**
- **Image Path:** Temporary file path (connect to next node)
- **Width/Height:** Image dimensions
- **Success:** True if loaded successfully

**Tips:**
- Use screenshots from Allplan viewport
- Or use hand-drawn sketches
- Supported formats: PNG, JPG, TIFF, BMP

---

### AI Render Basic Node

**Purpose:** Generate photorealistic architectural renders using Google's Nano Banana AI.

**Inputs:**

- **Input Image Path:** Connect from Load Image node
- **Prompt:** Describe what you want to see in the render
  - Example: "Modern glass facade building with landscaping, people, cars, photorealistic rendering"
  - Be specific but concise
  - Natural language works best

- **Style Preset:** Choose architectural style
  - **Modern:** Contemporary, clean lines, glass
  - **Classical:** Ornate details, columns, symmetry
  - **Industrial:** Exposed steel, concrete, brick
  - **Parametric:** Complex geometries, computational design
  - **Sustainable:** Green architecture, vegetation
  - **Minimalist:** Simple forms, monochromatic
  - **Brutalist:** Raw concrete, massive forms
  - **Organic:** Natural forms, curves

- **Lighting Preset:** Time of day / lighting condition
  - **Dawn:** Morning light, golden hour, warm tones
  - **Noon:** Bright sun, sharp shadows, high contrast
  - **Sunset:** Orange/pink sky, dramatic atmosphere
  - **Night:** Artificial lights, illuminated windows
  - **Overcast:** Soft diffused light, no harsh shadows
  - **Dramatic:** Strong contrast, theatrical lighting

- **Resolution:** Output quality
  - **1K (1024x1024):** Fast preview, draft quality
  - **2K (2048x2048):** Balanced quality/speed (RECOMMENDED)
  - **4K (4096x4096):** Highest quality, slower, more expensive

- **Use Nano Banana Pro:**
  - **False (default):** Use Nano Banana (Flash) - $0.039 per image
  - **True:** Use Nano Banana Pro - $0.13-0.24 per image (3-6x cost but highest quality)

**Outputs:**
- **Rendered Image Path:** Path to AI-generated render
- **Cost:** Actual API cost in USD
- **Process Time:** How long generation took
- **Success:** True if successful

**Tips:**
- Start with Nano Banana (Flash) to iterate quickly
- Use Nano Banana Pro for final high-quality renders
- 2K resolution is usually sufficient for most purposes
- Be patient - generation takes 30-90 seconds depending on resolution
- Check logs for detailed progress information

---

### Save Image Node

**Purpose:** Save the rendered image to a specific location with custom filename.

**Inputs:**
- **Image Path:** Connect from AI Render node
- **Output Path:** Where to save (click "..." to browse)
- **Format:** PNG (lossless) or JPEG (smaller file)
- **JPEG Quality:** 1-100 (higher = better, only for JPEG)
- **Add Timestamp:** Automatically add timestamp to filename to avoid overwriting

**Outputs:**
- **Saved Path:** Final file location
- **File Size:** Size in kilobytes
- **Success:** True if saved

**Tips:**
- PNG is recommended for maximum quality
- Enable "Add Timestamp" to keep all variations
- Default output directory: `C:\Allplan_Output\`

---

### Preview Image Node

**Purpose:** Quickly preview the image in your system's default image viewer.

**Inputs:**
- **Image Path:** Connect from Save Image node
- **Auto Open:** Enable to automatically open preview

**Outputs:**
- **Previewed:** True if preview was shown

**Tips:**
- Useful for quick checking during workflow development
- Disable Auto Open if running batch workflows

---

## 💰 Cost Management

### API Pricing

- **Nano Banana (Flash):** ~$0.039 per image (all resolutions)
- **Nano Banana Pro:** $0.134 per 1K-2K image, $0.240 per 4K image

### Budget Control

The plugin tracks your monthly costs automatically.

**Set budget limit in `.env`:**
```env
MAX_MONTHLY_COST_USD=100.0
```

The plugin will stop if you exceed this limit.

**View costs:**
Check the log file: `C:\Temp\AllplanRenderAI\allplan_render_ai.log`

### Cost Optimization Tips

1. **Use Nano Banana (Flash) for iteration** - Much cheaper, still good quality
2. **Start with 1K or 2K** - 4K is often overkill
3. **Use Nano Banana Pro only for finals** - Save the expensive renders for when you're happy with the result
4. **Batch similar renders** - Iterate on prompts before jumping to high resolution

**Example workflow:**
- 5x iterations with Flash @ 1K: 5 × $0.039 = $0.195
- 1x final with Pro @ 4K: 1 × $0.240 = $0.240
- **Total: $0.435** for a refined final render

---

## 🐛 Troubleshooting

### "Configuration invalid - check API keys"

**Problem:** Gemini API key not configured.

**Solution:**
1. Check that `.env` file exists in the plugin directory
2. Verify `GOOGLE_GEMINI_API_KEY` is set correctly
3. Get API key from: https://aistudio.google.com/app/apikey
4. Restart Allplan after updating `.env`

---

### "Input image not found"

**Problem:** The input image path is invalid or file doesn't exist.

**Solution:**
1. Use "Load Image" node to load the file first
2. Connect the "Image Path" output to "AI Render" input
3. Check that the file path is correct and file exists

---

### "Monthly budget limit exceeded"

**Problem:** You've reached the cost limit set in configuration.

**Solution:**
1. Check `C:\Temp\AllplanRenderAI\cost_tracking.json` to see current costs
2. Increase limit in `.env`: `MAX_MONTHLY_COST_USD=200.0`
3. Or wait until next month (costs reset monthly)

---

### Nodes don't appear in Visual Scripting

**Problem:** Nodes not visible in Allplan Visual Scripting Library palette.

**Solution:**
1. Verify files are in correct location:
   `C:\ProgramData\Nemetschek\Allplan\2025\Std\VisualScripts\AllplanRenderAI\`
2. Check that all three files exist for each node:
   - `NodeName.py`
   - `NodeName.pypsub`
   - `NodeName.xml`
3. Restart Allplan
4. Look under category "AI Rendering" in the Library palette

---

### Generation fails or times out

**Problem:** AI render generation fails or takes too long.

**Solution:**
1. Check internet connection
2. Verify API key is valid
3. Try lower resolution (1K instead of 4K)
4. Check Google Gemini API status
5. Review logs for detailed error: `C:\Temp\AllplanRenderAI\allplan_render_ai.log`

---

## 📊 Tips for Best Results

### Prompt Writing

**Good prompts:**
✅ "Modern glass facade office building with landscaped plaza, people walking, cars, photorealistic rendering, sunny day"

✅ "Classical villa with columns, symmetrical design, white marble, formal garden, clear blue sky"

✅ "Industrial warehouse conversion, exposed brick, large windows, wooden ceiling beams, atmospheric lighting"

**Less effective prompts:**
❌ "Make it look good"
❌ "Render"
❌ "Building"

**Best practices:**
- Be specific about materials (glass, concrete, wood, etc.)
- Include context elements (people, cars, vegetation)
- Mention desired atmosphere (sunny, dramatic, peaceful)
- Keep it concise but descriptive (1-3 sentences)

---

### Style Selection

- **Modern:** Best for contemporary projects, clean aesthetics
- **Classical:** Historic buildings, formal architecture
- **Industrial:** Adaptive reuse, loft conversions, raw materials
- **Parametric:** Cutting-edge design, complex forms
- **Sustainable:** Green buildings, biophilic design

Mix with lighting presets for different moods!

---

### Resolution Strategy

1. **Draft phase (1K):** Quick iterations, test prompts and styles
2. **Review phase (2K):** Show to clients, internal reviews
3. **Final presentation (4K with Pro):** Competition entries, marketing materials

---

## 🔜 What's Coming Next

### MVP2: Material Mapping (Week 2)
- Segmentation nodes
- Material application
- Variation studies

### MVP3: Photoinsertion (Week 3)
- Google Maps integration
- Context insertion
- Street View backgrounds

### MVP4: Advanced Features (Week 4)
- Inpainting for editing
- Batch processing
- Advanced utilities

---

## 📞 Support

- **Documentation:** Check `Docs/` folder
- **Logs:** `C:\Temp\AllplanRenderAI\allplan_render_ai.log`
- **Issues:** Submit via GitHub Issues
- **Community:** Allplan Connect Visual Scripting forum

---

## ✅ Quick Checklist

Before starting your first render:

- [ ] Dependencies installed (`python install_dependencies.py`)
- [ ] `.env` file configured with Gemini API key
- [ ] Files copied to Allplan VisualScripts folder
- [ ] Allplan restarted
- [ ] Nodes visible in Visual Scripting Library
- [ ] Test image ready (viewport screenshot or sketch)
- [ ] Output directory exists (`C:\Allplan_Output\`)

**You're ready to create AI renders!** 🎉

---

**Version:** MVP1
**Last Updated:** 2025-11
**Model:** Nano Banana / Nano Banana Pro (Google Gemini)
