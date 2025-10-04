#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sora Prompt Maker - Web Edition (Production Version)
Based on OpenAI's documented best practices and architectural insights
"""
from flask import Flask, render_template, jsonify, request
import json
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Template definitions - optimized based on OpenAI research
TEMPLATES = [
    {
        "name": "Cinematic Moment (Single Shot)",
        "description": "50-100 words. One subject, clear camera move. Optimized for Sora's spacetime patch architecture.",
        "guidance": "Start with subject/action, add setting, then layer technical specs. Use film terminology.",
        "fields": [
            {"id": "Subject", "label": "Subject (3-5 distinctive features)", "type": "text", 
             "default": "woman in black leather jacket, long red dress, sunglasses, red lipstick",
             "tip": "Avoid exhaustive detail. Focus on 3-5 distinctive elements."},
            {"id": "Action", "label": "Action (simple, specific verb phrase)", "type": "text", 
             "default": "walks confidently down the street",
             "tip": "Use precise verbs. 'Ambling' beats 'walking slowly and gradually.'"},
            {"id": "Setting", "label": "Setting (layered depth: fore/mid/background)", "type": "text", 
             "default": "Tokyo street filled with warm glowing neon signage at dusk; damp reflective pavement creating mirror effects",
             "tip": "Describe depth layers. Include atmospheric elements (weather, time, particles)."},
            {"id": "Camera", "label": "Camera Movement", "type": "choice", "choices": [
                "locked-off static shot", "slow dolly-in", "slow dolly-out", "tracking shot following subject",
                "gentle crane rise", "crane shot descending", "steadicam smooth movement", 
                "handheld with subtle jitter", "circling orbit shot", "low angle looking up", "high angle looking down"
            ], "default": "tracking shot following subject",
             "tip": "Use named movements, not mathematical paths. Complex trajectories struggle."},
            {"id": "Lens", "label": "Lens & Focus", "type": "text", 
             "default": "35mm f/2.8, shallow depth of field, focus locked on subject eyes",
             "tip": "Specify focal length, aperture, DOF. Use terms like 'bokeh', 'deep focus', 'rack focus at 5s'."},
            {"id": "Lighting", "label": "Lighting (quality/direction/temp)", "type": "text", 
             "default": "golden hour creating warm glow; soft diffused light with practical neon sources",
             "tip": "Use industry terms: golden hour, three-point lighting, rim lighting, volumetric."},
            {"id": "Physics", "label": "Physics & Materials", "type": "text", 
             "default": "light breeze 6-8 mph from camera left; wet asphalt with reflections; leather jacket with subtle texture",
             "tip": "Specify wind speed/direction, materials, surface properties. Sora simulates physics—describe it accurately."},
            {"id": "Look", "label": "Visual Style & Format", "type": "text", 
             "default": "shot on 35mm film; photorealistic with subtle film grain; vivid colors; cinematic widescreen 16:9",
             "tip": "Reference film stocks (35mm, 70mm, Super 8), formats (IMAX, anamorphic), grading (vivid, desaturated)."},
            {"id": "Audio", "label": "Audio (Sora 2 only)", "type": "text", 
             "default": "ambient city sounds; distant traffic; rain patter; footsteps on wet pavement; no dialogue",
             "tip": "Describe ambience, foley, music mood. Avoid 'many people speaking at once'—keep casts small."},
            {"id": "Duration", "label": "Duration Hint", "type": "choice", 
             "choices": ["quick moment (3-5s)", "standard scene (8-12s)", "extended sequence (15-20s)"],
             "default": "standard scene (8-12s)",
             "tip": "Implied through action complexity. Simple actions = brief, complex narratives = longer."},
            {"id": "Exclusions", "label": "Exclusions (what to avoid)", "type": "text", 
             "default": "no fast whip pans; no extra characters entering frame; no jump cuts; no branded products",
             "tip": "Be specific about what NOT to include. Helps constrain the generation."},
        ],
        "template": (
            "{Subject} {Action}. {Setting}. "
            "Camera: {Camera}; Lens: {Lens}. "
            "Lighting: {Lighting}. "
            "Physics: {Physics}. "
            "Visual style: {Look}. "
            "Audio: {Audio}. "
            "Pacing: {Duration}. "
            "Exclude: {Exclusions}"
        ),
    },
    {
        "name": "Advanced Format (Sora 2 Structured)",
        "description": "Separates conceptual vision from technical specs. 80-150 words. For complex shots.",
        "guidance": "Two-part structure: describe the scene conceptually, then specify technical execution separately.",
        "fields": [
            {"id": "Vision", "label": "Primary Vision (layered visual concepts)", "type": "multiline", 
             "default": "First read: a dragon slicing past serrated ice spires, wingtip vortices peeling spindrift; second read: the glacier's fractured sheet falling away to a cobalt fjord",
             "tip": "Describe in layers. What's the primary action? What's the secondary visual interest?"},
            {"id": "Subject", "label": "Subject Detail", "type": "text", 
             "default": "creature expressing predatory calm; obsidian scales catching pale arctic light",
             "tip": "Emotions/demeanor work better than exact facial expressions. 'Expressing joy' > 'smiling widely'."},
            {"id": "Environment", "label": "Environment (spatial relationships)", "type": "text", 
             "default": "foreground: fractured ice shelf; mid-ground: towering spires; background: mountain range fading into mist",
             "tip": "Explicitly state foreground/mid/background. Helps Sora's 3D consistency."},
            {"id": "Camera", "label": "Camera Execution", "type": "text", 
             "default": "tracking shot; low camera view is stunning capturing the large creature with beautiful photography",
             "tip": "Combine movement type with angle/perspective. Avoid precise trajectory math."},
            {"id": "TechnicalSpecs", "label": "Format & Technical Specifications", "type": "text", 
             "default": "5.0s; 4K; 180° shutter; large-format digital sensor emulation with crisp micro-contrast; very fine grain",
             "tip": "Duration, resolution, shutter angle, sensor type, grain level. Be specific."},
            {"id": "Lighting", "label": "Lighting Design", "type": "text", 
             "default": "overcast arctic light; soft shadows; edge lighting on ice crystals; volumetric light through mist",
             "tip": "Quality, direction, temperature, special effects (volumetric, rim, practicals)."},
            {"id": "Physics", "label": "Physics & Dynamics", "type": "text", 
             "default": "wind 15-20 mph creating snow drift; ice fragments tumbling realistically; water splash dynamics",
             "tip": "Specific forces, material behaviors, realistic interactions. Trust Sora's physics simulation."},
            {"id": "Audio", "label": "Audio Landscape", "type": "text", 
             "default": "howling wind; ice cracking; deep wing beats; distant avalanche rumble; close-mic wing vortices",
             "tip": "Layer sounds: ambience + specific foley + perspective (close-mic vs distant)."},
            {"id": "Exclusions", "label": "Exclusions", "type": "text", 
             "default": "no other creatures; no sudden camera jerks; no branded elements; no humans",
             "tip": "Prevents unwanted additions. Be explicit."},
        ],
        "template": (
            "PRIMARY VISION:\n{Vision}\n\n"
            "SUBJECT: {Subject}\n"
            "ENVIRONMENT: {Environment}\n\n"
            "CAMERA EXECUTION: {Camera}\n"
            "TECHNICAL SPECS: {TechnicalSpecs}\n"
            "LIGHTING: {Lighting}\n"
            "PHYSICS: {Physics}\n"
            "AUDIO: {Audio}\n\n"
            "EXCLUSIONS: {Exclusions}"
        ),
    },
    {
        "name": "Three-Shot Sequence",
        "description": "Multi-beat narrative. 100-150 words total. Maintains character consistency.",
        "guidance": "Sora excels at maintaining visual style across shots. Describe shot progression with temporal markers.",
        "fields": [
            {"id": "Character", "label": "Character (consistent across shots)", "type": "text", 
             "default": "30s engineer in charcoal hoodie, focused but warm demeanor",
             "tip": "Keep character description consistent. Sora maintains visual identity across shots."},
            {"id": "GlobalLook", "label": "Global Look & Color", "type": "text", 
             "default": "shot on 35mm film; natural color with subtle warmth; fine texture retention",
             "tip": "Applied to all shots. Maintains aesthetic coherence."},
            
            {"id": "S1_Action", "label": "Shot 1 (0-3s): Action & Setting", "type": "multiline", 
             "default": "Wide establishing shot: character enters cozy workshop, window light streaming in; background shelves with tools visible",
             "tip": "Establish context. Wide shots set the scene."},
            {"id": "S1_Camera", "label": "Shot 1: Camera & Lens", "type": "text", 
             "default": "locked-off wide shot; 24mm f/4; deep focus",
             "tip": ""},
            {"id": "S1_Light", "label": "Shot 1: Lighting & Physics", "type": "text", 
             "default": "natural window key from camera left; warm practicals in background; dust particles floating in light beam",
             "tip": ""},
            {"id": "S1_Audio", "label": "Shot 1: Audio", "type": "text", 
             "default": "quiet room tone; door closing sound; distant workshop ambience",
             "tip": ""},
            
            {"id": "S2_Action", "label": "Shot 2 (3-7s): Action & Setting", "type": "multiline", 
             "default": "Medium shot: character sits at workbench, notices a problem, picks up tool thoughtfully",
             "tip": "Build narrative. Medium shots show character behavior."},
            {"id": "S2_Camera", "label": "Shot 2: Camera & Lens", "type": "text", 
             "default": "slow dolly-in; 50mm f/2; focus on character face with background blur",
             "tip": ""},
            {"id": "S2_Light", "label": "Shot 2: Lighting & Physics", "type": "text", 
             "default": "key light from window maintained; soft edge kicker on tool; gentle head tilt micro-behavior",
             "tip": ""},
            {"id": "S2_Audio", "label": "Shot 2: Audio", "type": "text", 
             "default": "character exhales softly; tool clinking; one line of dialogue: 'we can do this' (reassuring tone)",
             "tip": ""},
            
            {"id": "S3_Action", "label": "Shot 3 (7-10s): Action & Setting", "type": "multiline", 
             "default": "Close-up: character smiles with realization, begins working with tool confidently",
             "tip": "Resolution. Close-ups show emotion and detail."},
            {"id": "S3_Camera", "label": "Shot 3: Camera & Lens", "type": "text", 
             "default": "locked-off close-up; 85mm f/1.8; shallow DOF, eyes in focus",
             "tip": ""},
            {"id": "S3_Light", "label": "Shot 3: Lighting & Physics", "type": "text", 
             "default": "soft key maintained; specular highlights on metal tool; subtle blink every 3s",
             "tip": ""},
            {"id": "S3_Audio", "label": "Shot 3: Audio", "type": "text", 
             "default": "tool engaging with work; satisfied 'hmm' sound; workshop ambience continues",
             "tip": ""},
            
            {"id": "Exclusions", "label": "Global Exclusions", "type": "text", 
             "default": "no other faces; no sudden camera moves; no jump cuts; no hand close-ups (hands are problematic)",
             "tip": "Hands and complex choreography struggle. Keep simple or wide."},
        ],
        "template": (
            "CHARACTER: {Character}\n"
            "GLOBAL LOOK: {GlobalLook}\n"
            "EXCLUSIONS: {Exclusions}\n\n"
            "SHOT 1 (0-3s) - ESTABLISHING:\n"
            "{S1_Action}\n"
            "Camera: {S1_Camera}\n"
            "Lighting: {S1_Light}\n"
            "Audio: {S1_Audio}\n\n"
            "SHOT 2 (3-7s) - DEVELOPMENT:\n"
            "{S2_Action}\n"
            "Camera: {S2_Camera}\n"
            "Lighting: {S2_Light}\n"
            "Audio: {S2_Audio}\n\n"
            "SHOT 3 (7-10s) - RESOLUTION:\n"
            "{S3_Action}\n"
            "Camera: {S3_Camera}\n"
            "Lighting: {S3_Light}\n"
            "Audio: {S3_Audio}"
        ),
    },
    {
        "name": "Product Hero Shot",
        "description": "Macro product beauty shot. 60-80 words. Controlled lighting and materials.",
        "guidance": "Emphasize material properties, reflections, and physics. Avoid fingerprints/dust in exclusions.",
        "fields": [
            {"id": "Product", "label": "Product (material/finish/brand-agnostic)", "type": "text", 
             "default": "sleek smartwatch with brushed aluminum body and sapphire crystal glass display",
             "tip": "Avoid brand names (never render accurately). Use generic descriptions with material detail."},
            {"id": "Surface", "label": "Surface & Environment", "type": "text", 
             "default": "dark matte slate surface with soft reflections; minimal background clutter",
             "tip": "Describe surface properties and how they interact with product (reflections, shadows)."},
            {"id": "HeroAction", "label": "Hero Motion", "type": "choice", "choices": [
                "slow 360° turntable rotation", "condensation forming and rolling", "soft reveal from shadow to light",
                "gentle product levitation", "water droplets hitting surface"
            ], "default": "slow 360° turntable rotation",
             "tip": "Simple, elegant motion. Complex physics can fail—keep interactions straightforward."},
            {"id": "Camera", "label": "Camera & Lens", "type": "text", 
             "default": "macro rail push-in; 100mm macro f/4; shallow DOF focused on brand detail",
             "tip": "Macro lenses for detail. Specify focus point explicitly."},
            {"id": "Lighting", "label": "Lighting Setup", "type": "text", 
             "default": "soft top key light; edge kicker from camera right; controlled specular highlights on glass and metal",
             "tip": "Product photography lighting: key, fill, rim, kicker. Control reflections."},
            {"id": "Color", "label": "Color & Grading", "type": "text", 
             "default": "neutral balanced color; brand palette emphasis; avoid teal/orange bias",
             "tip": "Mention color accuracy, brand colors, avoid common grading clichés if needed."},
            {"id": "Physics", "label": "Material Physics", "type": "text", 
             "default": "condensation beads form slowly on glass; gravity-consistent droplet roll; aluminum retains matte finish",
             "tip": "How materials behave: water on glass, fabric drape, metal reflections. Be realistic."},
            {"id": "Audio", "label": "Audio", "type": "text", 
             "default": "subtle room tone; single 'click' SFX as product feature activates; no music",
             "tip": "Minimal but purposeful. Product sounds + ambience."},
            {"id": "Format", "label": "Format & Duration", "type": "text", 
             "default": "vertical 9:16 for social media; 8-10 seconds; 4K resolution",
             "tip": "Sora handles various aspect ratios natively. Specify for optimal composition."},
            {"id": "Exclusions", "label": "Exclusions", "type": "text", 
             "default": "no fingerprints; no lens breathing; no dust particles; no visible supports; no brand text close-ups",
             "tip": "Critical for product work. List all imperfections to avoid."},
        ],
        "template": (
            "PRODUCT: {Product}\n"
            "{HeroAction} on {Surface}.\n\n"
            "CAMERA: {Camera}\n"
            "LIGHTING: {Lighting}\n"
            "COLOR: {Color}\n\n"
            "MATERIAL PHYSICS: {Physics}\n"
            "AUDIO: {Audio}\n"
            "FORMAT: {Format}\n\n"
            "EXCLUDE: {Exclusions}"
        ),
    },
    {
        "name": "Image-to-Video Animation",
        "description": "Animate a still image. 40-60 words. Preserve composition, add subtle motion.",
        "guidance": "Clearly state what must stay fixed vs. what should move. Sora excels at gentle parallax and atmospheric animation.",
        "fields": [
            {"id": "SourceDesc", "label": "Source Image Description", "type": "multiline", 
             "default": "misty forest cabin beside calm lake with perfect reflection; early morning fog; warm window light visible",
             "tip": "Describe the still image content. This anchors the generation."},
            {"id": "Preserve", "label": "Preserve (must not change)", "type": "text", 
             "default": "composition framing; cabin structure; overall color palette; lake position",
             "tip": "What stays locked. Architecture, key subjects, core composition."},
            {"id": "Animate", "label": "Animate (what moves)", "type": "text", 
             "default": "gentle camera push-in creating parallax; tree leaves rustle softly; water ripples across lake surface; mist drifts slowly",
             "tip": "Subtle motion works best. Avoid adding new objects or changing faces."},
            {"id": "Camera", "label": "Camera Treatment", "type": "choice", 
             "choices": ["locked-off (no camera move)", "subtle push-in", "gentle parallax shift", "slight drift"],
             "default": "subtle push-in",
             "tip": "Minimal camera movement. Sora adds natural motion without fighting the source."},
            {"id": "Physics", "label": "Environmental Physics", "type": "text", 
             "default": "wind 5-7 mph from left; natural leaf movement; realistic water ripple propagation",
             "tip": "Describe natural forces. Keep physics simple and plausible."},
            {"id": "Audio", "label": "Audio (match visuals)", "type": "text", 
             "default": "matching forest ambience; distant birds; soft wind through trees; gentle water lapping",
             "tip": "Audio should feel natural for the scene. No jarring music unless appropriate."},
            {"id": "Exclusions", "label": "Exclusions", "type": "text", 
             "default": "no new objects appearing; no animals entering; no structural changes; no lighting time shifts",
             "tip": "Prevent scope creep. Lock down what shouldn't be added."},
        ],
        "template": (
            "SOURCE IMAGE: {SourceDesc}\n\n"
            "PRESERVE: {Preserve}\n"
            "ANIMATE: {Animate}\n"
            "CAMERA: {Camera}\n"
            "PHYSICS: {Physics}\n"
            "AUDIO: {Audio}\n\n"
            "EXCLUDE: {Exclusions}"
        ),
    },
    {
        "name": "Loopable/Seamless Animation",
        "description": "Perfect loop design. 30-50 words. First and last frames must match.",
        "guidance": "Design cyclical motion. Locked camera prevents drift. Simple repeating actions work best.",
        "fields": [
            {"id": "Subject", "label": "Looping Subject/Action", "type": "multiline", 
             "default": "neon 'OPEN' sign flickers in consistent pattern; rain creates ripples in puddle below; cycle repeats every 2.5 seconds",
             "tip": "Describe the repeating cycle. Simple motions loop better than complex narratives."},
            {"id": "Camera", "label": "Camera (should be locked)", "type": "choice", 
             "choices": ["locked-off (required for clean loops)"],
             "default": "locked-off (required for clean loops)",
             "tip": "Camera drift breaks loops. Always lock camera position."},
            {"id": "LoopDesign", "label": "Loop Structure", "type": "text", 
             "default": "first and last frames visually identical; motion cycle duration 2.5s repeated 4 times for 10s total",
             "tip": "Specify cycle duration and repetition count. Helps Sora understand loop boundaries."},
            {"id": "Lighting", "label": "Lighting (must be consistent)", "type": "text", 
             "default": "night scene; steady neon glow; wet pavement reflections; no time-of-day progression",
             "tip": "Avoid lighting changes that imply time passing. Keep environment static."},
            {"id": "Physics", "label": "Cyclical Physics", "type": "text", 
             "default": "rain intensity steady; ripple patterns reset smoothly; neon flicker pattern repeats",
             "tip": "Physics should complete cycles. Ripples finish, rain is constant, etc."},
            {"id": "Audio", "label": "Audio (seamless loop)", "type": "text", 
             "default": "ambient rain loop; neon buzz; no transient sounds at loop point; crossfade-ready ambience",
             "tip": "Audio should loop without clicks/pops. Avoid one-time sounds at boundaries."},
            {"id": "Exclusions", "label": "Exclusions", "type": "text", 
             "default": "no camera drift; no time-of-day shift; no progressive changes; no entering/exiting subjects",
             "tip": "Anything that implies progression breaks the loop. Lock it all down."},
        ],
        "template": (
            "LOOPING SUBJECT: {Subject}\n"
            "CAMERA: {Camera}\n"
            "LOOP DESIGN: {LoopDesign}\n\n"
            "LIGHTING: {Lighting}\n"
            "PHYSICS: {Physics}\n"
            "AUDIO: {Audio}\n\n"
            "EXCLUDE: {Exclusions}"
        ),
    },
]

# Best practices and tips based on research
BEST_PRACTICES = {
    "optimal_length": "50-120 words for most prompts. More detail helps when precise, but avoid redundancy.",
    "structure": "Hierarchical: Subject/Action → Setting → Camera/Lighting → Technical Specs → Exclusions",
    "camera_movements": "Use named professional terms: 'tracking shot', 'dolly-in', 'crane shot'. Avoid mathematical trajectories.",
    "physics": "Describe realistic physics. Sora simulates—don't fight it. Specify materials, forces, realistic interactions.",
    "limitations": "Hands struggle (use wider shots), complex multi-character choreography fails (simplify), branded items don't render accurately (use generic descriptions).",
    "temporal_control": "Use sequence markers: 'First... then... finally.' Specify pacing through action complexity.",
    "audio": "Sora 2 only. Keep casts small, one speaker at a time. Layer ambience + foley + music/dialogue.",
    "exclusions": "Be explicit about what to avoid. Helps constrain generation and prevent unwanted additions.",
}

@app.route('/')
def index():
    """Serve the main application page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return jsonify({'error': 'Failed to load application'}), 500

@app.route('/api/templates')
def get_templates():
    """Return available prompt templates"""
    try:
        return jsonify(TEMPLATES)
    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        return jsonify({'error': 'Failed to fetch templates'}), 500

@app.route('/api/best_practices')
def get_best_practices():
    """Return best practices guide"""
    try:
        return jsonify(BEST_PRACTICES)
    except Exception as e:
        logger.error(f"Error fetching best practices: {e}")
        return jsonify({'error': 'Failed to fetch best practices'}), 500

@app.route('/api/ollama_models')
def get_ollama_models():
    """Get available Ollama models"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model.get('name', model.get('model', '')) for model in data.get('models', [])]
            return jsonify({'models': models, 'status': 'online'})
        return jsonify({'error': 'Failed to fetch models', 'status': 'error'}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Ollama not running', 'status': 'offline'}), 503
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Ollama request timed out', 'status': 'timeout'}), 504
    except Exception as e:
        logger.error(f"Unexpected error fetching Ollama models: {e}")
        return jsonify({'error': 'Unexpected error', 'status': 'error'}), 500

@app.route('/api/generate_prompt', methods=['POST'])
def generate_prompt():
    """Generate a prompt from template and field values"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        template_name = data.get('template')
        values = data.get('values', {})
        include_labels = data.get('include_labels', True)
        
        if not template_name:
            return jsonify({'error': 'Template name required'}), 400
        
        template = next((t for t in TEMPLATES if t['name'] == template_name), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        tpl_text = template['template']
        rendered = tpl_text.format(**values)
        
        if not include_labels:
            # Strip labels for cleaner output
            lines = []
            for line in rendered.splitlines():
                if ':' in line:
                    parts = line.split(':', 1)
                    label = parts[0].strip()
                    if label.isupper() or label.replace(' ', '').replace('/', '').replace('-', '').isalpha():
                        content = parts[1].strip()
                        if content:
                            lines.append(content)
                    else:
                        lines.append(line.strip())
                else:
                    if line.strip():
                        lines.append(line.strip())
            rendered = ' '.join(lines).strip()
        
        # Calculate word count
        word_count = len(rendered.split())
        
        return jsonify({
            'prompt': rendered,
            'word_count': word_count,
            'optimal': 50 <= word_count <= 120
        })
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        return jsonify({'error': 'Failed to generate prompt'}), 500

@app.route('/api/ollama_assist', methods=['POST'])
def ollama_assist():
    """AI-assisted prompt generation via Ollama"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_prompt = data.get('user_prompt', '')
        template_name = data.get('template')
        current_values = data.get('current_values', {})
        model = data.get('model', 'llama3.2')
        
        if not template_name:
            return jsonify({'error': 'Template name required'}), 400
        
        template = next((t for t in TEMPLATES if t['name'] == template_name), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # Build enhanced system prompt with research insights
        field_descriptions = '\n'.join([
            f"- {f['id']}: {f['label']}"
            + (f" (tip: {f['tip']})" if 'tip' in f else "")
            for f in template['fields']
        ])
        
        system_prompt = f"""You are an expert at creating Sora video generation prompts based on OpenAI's documented best practices.

TEMPLATE: {template_name}
{template.get('guidance', '')}

FIELDS TO FILL:
{field_descriptions}

USER'S CONCEPT: {user_prompt}

CURRENT VALUES:
{json.dumps(current_values, indent=2)}

BEST PRACTICES (apply these):
- Use professional film terminology: shot types, camera movements, lighting terms
- Describe physics realistically: materials, forces, realistic interactions
- Layer information: foreground/mid-ground/background relationships
- Specify temporal progression for sequences
- Avoid: branded products, complex hand movements, overly specific physics
- Keep optimal prompt length: 50-120 words total when all fields combined
- Be specific and precise—every word should add value

Based on the user's concept, suggest creative but technically sound values for ALL fields.
Output ONLY valid JSON with field IDs as keys. No explanations, just the JSON."""

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': system_prompt,
                'stream': False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '')
            
            # Try to extract JSON from response
            try:
                start = llm_response.find('{')
                end = llm_response.rfind('}') + 1
                if start != -1 and end > start:
                    suggestions = json.loads(llm_response[start:end])
                    return jsonify({'suggestions': suggestions})
            except json.JSONDecodeError:
                logger.warning(f"Could not parse LLM JSON response")
            
            return jsonify({'error': 'Could not parse LLM response', 'raw': llm_response}), 500
        else:
            return jsonify({'error': 'Ollama request failed', 'status': response.status_code}), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Could not connect to Ollama. Make sure Ollama is running on localhost:11434'}), 503
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Ollama request timed out'}), 504
    except Exception as e:
        logger.error(f"Error in Ollama assist: {e}")
        return jsonify({'error': 'Unexpected error'}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

def initialize_app():
    """Initialize application directories and resources"""
    try:
        Path('templates').mkdir(exist_ok=True)
        Path('static').mkdir(exist_ok=True)
        logger.info("Application directories initialized")
    except Exception as e:
        logger.error(f"Failed to initialize directories: {e}")
        raise

if __name__ == '__main__':
    try:
        initialize_app()
        
        print("\n" + "="*70)
        print("SORA PROMPT MAKER - PRODUCTION MODE")
        print("="*70)
        print("\nBased on OpenAI's documented best practices:")
        print("  ✓ 50-120 word optimal prompts")
        print("  ✓ Professional film terminology")
        print("  ✓ Physics-accurate descriptions")
        print("  ✓ Structured hierarchical prompting")
        print("\nServer running at: http://127.0.0.1:5000")
        print("(Local access only)")
        print("\nOptional: Start Ollama for AI-assisted prompt generation")
        print("   ollama run llama3.2")
        print("="*70 + "\n")
        
        app.run(host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        print(f"\n[CRITICAL ERROR] Application failed to start: {e}\n")
        exit(1)
