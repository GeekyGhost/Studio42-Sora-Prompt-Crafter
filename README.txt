# 🎬 Studio 42 - Sora Prompt Crafter

## "Mostly Harmless Prompt Generation"

A Hitchhiker's Guide to the Galaxy meets Star Trek LCARS inspired AI-powered prompt crafting tool for Sora video generation.

---

## 🚀 What's New

### Complete UI Overhaul - LCARS Design System
- **Studio 42 Branding** - Professional studio aesthetic
- **Star Trek LCARS Interface** - Iconic sci-fi UI with rounded pills, bold colors, and futuristic typography
- **Hitchhiker's Guide Easter Eggs** - "Don't Panic" badge, quirky messaging, terminal aesthetics
- **Interactive Elements** - Animated status indicators, glowing effects, hover states
- **Color Palette**: 
  - Primary: Orange/Amber (#ffaa00)
  - Accents: Purple (#9966cc), Pink (#cc6699), Blue (#6699cc)
  - Background: Deep black with gradient panels

### 🖼️ Vision Model Support (NEW!)
- **Image Upload** - Drag & drop or click to upload reference images
- **Vision Model Detection** - Automatically shows upload option when vision models available
- **Models Supported**: llama3.2-vision, llava, moondream, and other vision-capable models
- **Image Preview** - See uploaded image with file info
- **AI Integration** - Vision models analyze uploaded images to inform prompt generation

### ⚙️ Generation Controls
- **Temperature** (0-2) - Creativity level slider
- **Top-P** (0-1) - Response diversity control  
- **Top-K** (1-100) - Token selection pool size
- **Seed** (optional) - Reproducibility control for identical outputs
- All controls properly labeled with explanations

### 🎨 UI Features
- **Left Sidebar** - Quick navigation pills to major sections
- **System Status Block** - Real-time status of Ollama, Templates, and Vision capabilities
- **Collapsible Panels** - Clean organization of advanced controls
- **Terminal-Style Output** - Green-on-black output display
- **Animated Elements** - Pulsing indicators, floating badges, smooth transitions
- **Responsive Design** - Works on desktop, tablet, and mobile

---

## 📋 Files Updated

### 1. `templates/index.html`
**Complete redesign with:**
- LCARS-inspired CSS styling system
- Image upload functionality with drag-and-drop
- Vision model detection and conditional UI
- Enhanced status indicators and system monitoring
- Terminal-style output display
- Improved mobile responsiveness

### 2. `app.py` (Backend)
**New features:**
- Image upload handling for vision models
- Vision model detection logic
- Base64 image encoding and transmission to Ollama
- Enhanced logging for image operations
- Proper error handling for image processing

### 3. `requirements.txt` (No Changes Needed)
Already includes:
- Flask ≥3.0.0
- waitress ≥2.1.2 (production WSGI server)
- requests ≥2.31.0

---

## 🎯 How to Use Vision Features

### Setup
1. Make sure you have a vision-capable model installed:
   ```bash
   ollama pull llama3.2-vision
   # or
   ollama pull llava
   # or
   ollama pull moondream
   ```

2. Start Ollama:
   ```bash
   ollama serve
   ```

3. Run the app:
   ```bash
   run.bat
   ```

### Using Vision Mode
1. **Select a vision model** from the dropdown (will show VISION in name)
2. **Upload reference image** - The upload zone will appear automatically
3. **Drag & drop** an image or click to browse
4. **Describe your concept** in the text area - mention elements from the image
5. **Adjust generation controls** if desired
6. **Click "Engage AI Neural Network"**
7. Review and adjust the AI-generated fields
8. **Generate final prompt**

### Example Vision Workflow
```
1. Upload: Photo of a cyberpunk street scene
2. Prompt: "Transform this into a cinematic Sora prompt 
           with dramatic lighting and rain effects"
3. AI analyzes the image and fills template fields based on
   visual elements it detects
4. You refine the output and generate final prompt
```

---

## 🎨 Design Philosophy

### LCARS Aesthetic
- **Rounded Pill Buttons** - Star Trek signature style
- **Bold Typography** - Orbitron font for headers, Roboto Mono for content
- **Color-Coded Elements** - Functional use of color (status, navigation, alerts)
- **Angular Panels** - Sharp corners mixed with rounded elements
- **Status Indicators** - Blinking lights and animated elements

### Hitchhiker's Guide Elements
- **"Don't Panic" Badge** - Floating reminder in corner
- **Quirky Messaging** - "Mostly Harmless Prompt Generation"
- **Terminal Aesthetics** - Green-on-black output terminal
- **British Sci-Fi Humor** - Subtle nods throughout UI text

---

## 🛠️ Technical Details

### Vision Model Integration
```javascript
// Frontend sends image as base64
{
  user_prompt: "description...",
  model: "llama3.2-vision",
  image: {
    data: "data:image/png;base64,iVBORw0KG...",
    name: "reference.png",
    size: 245678
  },
  temperature: 1.0,
  top_p: 0.9,
  top_k: 40
}
```

```python
# Backend processes for Ollama
request_payload = {
    'model': model,
    'prompt': system_prompt,
    'stream': False,
    'options': options,
    'images': [base64_image_data]  # Vision models only
}
```

### Color Variables (CSS)
```css
Primary: #ffaa00 (Amber)
Secondary: #9966cc (Purple)
Accent 1: #cc6699 (Pink)
Accent 2: #6699cc (Blue)
Success: #00ff00 (Green)
Error: #ff3366 (Red)
Background: #000000 (Black)
Panel: #1a1a1a - #2d2d2d (Gradient)
```

---

## 🎮 Interactive Features

### Status Monitoring
- **Ollama Connection** - Real-time status check
- **Template Loading** - Shows when templates are ready
- **Vision Capability** - Detects vision-capable models

### Navigation
- **Sidebar Quick Nav** - Jump to any section
- **Smooth Scrolling** - Animated section transitions
- **Active Highlighting** - Current section indicated

### Animations
- **Pulse Glow** - Studio 42 badge
- **Blinking Status** - System indicators
- **Float Effect** - Don't Panic badge
- **Hover States** - All interactive elements
- **Loading Spinners** - During AI processing

---

## 🔧 Configuration

### Default Generation Settings
```javascript
Temperature: 1.0  // Higher creativity for prompts
Top-P: 0.9       // Wide diversity
Top-K: 40        // Balanced token pool
Seed: null       // Random (for variation)
```

### Recommended Vision Models
- **llama3.2-vision** - Best all-around (if available)
- **llava** - Strong visual understanding
- **moondream** - Lightweight, fast

---

## 📱 Responsive Breakpoints

- **Desktop** (1024px+) - Full sidebar, expanded layout
- **Tablet** (768-1024px) - Hidden sidebar, streamlined
- **Mobile** (<768px) - Stacked layout, compact controls

---

## 🐛 Troubleshooting

### Vision Upload Not Showing?
- Check if you have vision models installed: `ollama list`
- Model name must contain: "vision", "llava", or "moondream"
- Restart app after installing vision models

### Image Not Processing?
- Supported formats: JPG, PNG, GIF, WebP
- Max size: Limited by browser (typically 10MB+)
- Check browser console for errors

### LCARS UI Not Loading?
- Clear browser cache
- Check if CSS loaded (view page source)
- Ensure all font imports successful

---

## 🎓 Best Practices

### For Vision-Guided Prompts
1. Use clear, well-lit reference images
2. Describe what to keep vs. change from image
3. Mention specific elements visible in photo
4. Let AI interpret visual style, you guide content

### For Template Selection
- **Single Shot** - Most scenes
- **Advanced Format** - Complex technical requirements
- **Product Hero** - Commercial/marketing
- **Image-to-Video** - When using vision models

### For Generation Controls
- **High creativity** (1.5-2.0) - Experimental, artistic
- **Medium creativity** (0.8-1.2) - Balanced (recommended)
- **Low creativity** (0.2-0.5) - Technical, precise
- **Leave seed blank** - For variation between runs

---

## 🚀 Future Enhancements

- [ ] Multi-image support for sequences
- [ ] Image-to-image style transfer previews
- [ ] Prompt history and favorites
- [ ] Export prompts to JSON/CSV
- [ ] Preset generation profiles
- [ ] More LCARS sound effects

---

## 📄 License

Part of the Studio 42 creative suite. For internal use.

---

**Don't Panic!** 🌟

*Made with ❤️ and a towel by Studio 42*