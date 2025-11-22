# Allplan Render AI - Visual Scripting Plugin

AI-powered architectural rendering plugin for Allplan using Nano Banana Pro (Google Gemini).

## Overview

This plugin provides a comprehensive node-based workflow system for Allplan Visual Scripting, enabling:
- AI-powered rendering with Google's Nano Banana / Nano Banana Pro
- Material segmentation and mapping
- Professional photoinsertion with Google Maps integration
- Natural language image editing with inpainting
- Batch processing and workflow automation

## Architecture

The plugin is built as a collection of custom Visual Scripting nodes that can be combined into workflows:

### Node Categories

1. **Core Nodes** - Image I/O and viewport capture
2. **AI Rendering** - Nano Banana integration for photorealistic rendering
3. **Segmentation** - AI-powered material detection and segmentation
4. **Photoinsertion** - Context insertion with Google Maps backgrounds
5. **Inpainting** - Natural language editing with Imagen 3
6. **Utilities** - Helper nodes for image processing and workflow management

## Installation

### Prerequisites

- Allplan 2025 (or 2024)
- Python 3.9+ (included with Allplan)
- Google Cloud account with API access

### Setup

1. **Install Python Dependencies**

Run the installation script:
```bash
python install_dependencies.py
```

This will install the required packages to Allplan's Python environment:
- Pillow (PIL)
- opencv-python-headless
- google-generativeai
- google-cloud-aiplatform
- googlemaps
- requests
- python-dotenv
- numpy

2. **Configure API Keys**

Copy `.env.template` to `.env` and fill in your API keys:
```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_MAPS_API_KEY=your_maps_api_key
DEBUG_MODE=false
```

3. **Copy Files to Allplan**

Copy the `VisualScripts` folder to:
```
C:\ProgramData\Nemetschek\Allplan\2025\Std\VisualScripts\AllplanRenderAI\
```

4. **Restart Allplan**

The custom nodes will appear in the Visual Scripting Library palette under category "AI Rendering".

## Quick Start

### MVP1: Basic AI Rendering

1. Open Allplan Visual Scripting
2. Load the template: `WorkflowTemplates/BasicRendering.avsprj`
3. Set your viewport in Allplan
4. Run the script

The workflow will:
- Capture your current viewport
- Generate an AI render using Nano Banana Pro
- Save the result to your output folder
- Preview the rendered image

## Workflow Templates

- **BasicRendering.avsprj** - Simple viewport to AI render
- **MaterialVariation.avsprj** - Create material variations (Coming in MVP2)
- **Photoinsertion.avsprj** - Insert building into real photo (Coming in MVP3)
- **BatchMultiView.avsprj** - Generate multiple context views (Coming in MVP4)
- **IterativeRefinement.avsprj** - Iterative editing workflow (Coming in MVP4)

## Node Reference

See [Docs/NodeReference.md](Docs/NodeReference.md) for complete node documentation.

## Development Roadmap

- [x] **MVP1: Basic AI Rendering** (Week 1)
  - Core I/O nodes
  - Nano Banana integration
  - Basic workflow template

- [ ] **MVP2: Material Mapping** (Week 2)
  - Segmentation nodes
  - Material application
  - Variation workflows

- [ ] **MVP3: Photoinsertion** (Week 3)
  - Background management
  - Google Maps integration
  - Context insertion

- [ ] **MVP4: Advanced Features** (Week 4)
  - Inpainting nodes
  - Utility nodes
  - Advanced templates

## Cost Estimates

Typical costs per operation (using Google APIs):
- Basic render (2K, Nano Banana): ~$0.039
- Pro render (4K, Nano Banana Pro): ~$0.24
- Segmentation: ~$0.012
- Inpainting: ~$0.05-0.15
- Street View fetch: Free

Monthly usage (50 renders): ~$7-10/month

## Support

- Documentation: [Docs/UserGuide.md](Docs/UserGuide.md)
- Issues: Submit via GitHub Issues
- Forum: Allplan Connect Visual Scripting

## License

[License Type TBD]

## Credits

Developed for Allplan 2025 Visual Scripting
Powered by Google Gemini (Nano Banana Pro) and Imagen 3
