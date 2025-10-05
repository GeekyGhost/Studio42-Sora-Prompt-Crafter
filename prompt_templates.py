#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Templates for AI Video and Image Generation
Supports: SORA, WAN (2.1, 2.2, 2.5), QWEN Image Edit 2509, NANO BANANA (Gemini 2.5 Flash)
Based on research from Sora_Prompt_Research.md and wan_and_qwen.md
"""

# ==================== SORA TEMPLATES ====================
SORA_TEMPLATES = [
    {
        "name": "Cinematic Moment (Single Shot)",
        "model": "sora",
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
        "model": "sora",
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
        "model": "sora",
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
        "model": "sora",
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
        "model": "sora",
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
        "model": "sora",
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

# ==================== WAN TEMPLATES ====================
WAN_TEMPLATES = [
    {
        "name": "Wan Basic Video (Subject + Scene + Motion)",
        "model": "wan",
        "description": "Simple 3-part structure. 30-50 words. Perfect for quick 5-second generations.",
        "guidance": "Focus on ONE clear action. Keep it concise. Use Wan's prompt extension for quality boost.",
        "fields": [
            {"id": "Subject", "label": "Subject Description", "type": "text",
             "default": "Two anthropomorphic cats in comfy boxing gear and bright gloves",
             "tip": "3-5 distinctive features. Be specific but concise."},
            {"id": "Scene", "label": "Scene/Setting", "type": "text",
             "default": "spotlighted stage with cheering crowd in background",
             "tip": "Describe environment and atmosphere."},
            {"id": "Motion", "label": "Action/Motion (ONE primary action)", "type": "text",
             "default": "fight intensely, throwing punches and dodging",
             "tip": "Use specific verbs. ONE action per 5-second clip."},
        ],
        "template": "{Subject} {Motion} on {Scene}."
    },
    {
        "name": "Wan Cinematic (Full Control)",
        "model": "wan",
        "description": "Complete cinematic specification. 100-150 words. Professional quality.",
        "guidance": "Layer descriptions: Lighting + Camera + Subject + Motion + Style. Use prompt extension feature.",
        "fields": [
            {"id": "Lighting", "label": "Lighting Setup", "type": "choice",
             "choices": [
                 "sunny lighting, edge lighting, warm tones, soft light, daylight",
                 "artificial lighting, edge lighting, warm colors",
                 "moonlighting, side shadows, cool tones",
                 "firelight, warm glow, flickering shadows",
                 "fluorescent lighting, cool tones, overhead",
                 "mixed lighting, contrast, underlighting, night time"
             ],
             "default": "sunny lighting, edge lighting, warm tones, soft light, daylight",
             "tip": "Light source defines mood. Use Wan's specific terminology."},
            {"id": "Contrast", "label": "Contrast Level", "type": "choice",
             "choices": ["low contrast", "medium contrast", "high contrast"],
             "default": "medium contrast",
             "tip": "Low = soft/dreamy, High = dramatic/bold"},
            {"id": "ShotSize", "label": "Shot Size", "type": "choice",
             "choices": [
                 "extreme close-up",
                 "close-up",
                 "medium close-up",
                 "medium shot",
                 "medium wide",
                 "wide shot",
                 "extreme wide/establishing shot"
             ],
             "default": "medium close-up",
             "tip": "Determines framing and emotional connection."},
            {"id": "CameraAngle", "label": "Camera Angle", "type": "choice",
             "choices": [
                 "eye-level shot",
                 "high angle",
                 "low angle",
                 "dutch angle/tilt",
                 "aerial/bird's eye",
                 "over-the-shoulder"
             ],
             "default": "eye-level shot",
             "tip": "Affects power dynamics and perspective."},
            {"id": "TimeOfDay", "label": "Time of Day", "type": "choice",
             "choices": ["sunrise", "daylight", "golden hour", "sunset", "dusk", "night", "dawn"],
             "default": "daylight",
             "tip": "Changes color palette and atmosphere."},
            {"id": "Composition", "label": "Composition Style", "type": "choice",
             "choices": [
                 "center composition",
                 "rule of thirds",
                 "left-side composition",
                 "right-side composition",
                 "symmetrical",
                 "short-side composition"
             ],
             "default": "rule of thirds",
             "tip": "How elements are arranged in frame."},
            {"id": "Subject", "label": "Subject Detail", "type": "text",
             "default": "A black-haired Miao girl wearing ethnic minority clothing",
             "tip": "Include clothing, appearance, demeanor. 3-5 key details."},
            {"id": "Action", "label": "Action/Behavior", "type": "text",
             "default": "sits in a field of tall grass, gently swaying in the breeze",
             "tip": "Specific verbs. ONE primary action for 5-second clips."},
            {"id": "Environment", "label": "Environment (layered depth)", "type": "text",
             "default": "foreground: tall grass; mid-ground: two fluffy little donkeys; background: rolling hills",
             "tip": "Describe fore/mid/background explicitly for 3D depth."},
            {"id": "CameraMove", "label": "Camera Movement", "type": "choice",
             "choices": [
                 "static/fixed shot",
                 "camera pushes in",
                 "camera pulls back",
                 "slow dolly-in",
                 "tracking shot",
                 "pan left",
                 "pan right",
                 "tilt up",
                 "tilt down",
                 "arc shot",
                 "handheld camera"
             ],
             "default": "static/fixed shot",
             "tip": "Simple movements work best. Avoid complex trajectories."},
            {"id": "Lens", "label": "Lens Type", "type": "choice",
             "choices": [
                 "wide-angle lens",
                 "medium lens",
                 "telephoto/long-focus lens",
                 "fisheye lens"
             ],
             "default": "medium lens",
             "tip": "Affects perspective and depth compression."},
            {"id": "Style", "label": "Visual Style", "type": "choice",
             "choices": [
                 "photorealistic",
                 "2D anime style",
                 "3D cartoon style",
                 "cartoon style",
                 "oil painting style",
                 "watercolor painting",
                 "impressionistic style",
                 "pixel art style",
                 "cyberpunk",
                 "film noir",
                 "felt style",
                 "claymation style"
             ],
             "default": "photorealistic",
             "tip": "Overall aesthetic direction."},
            {"id": "ColorGrade", "label": "Color Grading", "type": "choice",
             "choices": [
                 "warm colors",
                 "cool colors",
                 "saturated colors",
                 "desaturated colors"
             ],
             "default": "warm colors",
             "tip": "Color palette sets emotional tone."},
        ],
        "template": (
            "{Lighting}, {Contrast}, {ShotSize}, {CameraAngle}, {TimeOfDay}, {Composition}. "
            "{Subject} {Action}. {Environment}. "
            "Camera: {CameraMove}; Lens: {Lens}. "
            "Visual style: {Style}, {ColorGrade}."
        )
    },
    {
        "name": "Wan 2.5 with Audio Sync",
        "model": "wan",
        "description": "Video with synchronized audio and dialogue. 120-180 words. Native lip-sync.",
        "guidance": "Wan 2.5's revolutionary feature: audio-video synchronization. Describe dialogue, ambient sounds, and timing clearly.",
        "fields": [
            {"id": "SceneSetup", "label": "Scene Setup & Lighting", "type": "multiline",
             "default": "Dimly lit basement on a rainy city night with flickering fluorescents, folding chairs, glowing laptops",
             "tip": "Set the atmosphere and environment."},
            {"id": "Characters", "label": "Characters Present", "type": "text",
             "default": "Hooded young filmmakers with vintage cameras, central character named Tyler",
             "tip": "Describe who is in the scene. Keep casts small (Wan limitation)."},
            {"id": "CameraSequence", "label": "Camera Movement Sequence", "type": "text",
             "default": "Starts wide on gritty basement, pushes slowly to medium on Tyler, holds on his intense face",
             "tip": "Describe camera progression through the scene."},
            {"id": "Dialogue", "label": "Dialogue with Actions", "type": "multiline",
             "default": "Tyler leans forward, speaking gravelly: 'The first rule of AI filmmaking: You DO talk about AI filmmaking.' Camera pulls back to show group's smirking nods.",
             "tip": "Speaker name, tone, exact dialogue in quotes, physical actions. ONE speaker at a time!"},
            {"id": "AmbientAudio", "label": "Background/Ambient Audio", "type": "text",
             "default": "rain hum, distant traffic, buzzing fluorescent lights, laptop fans, occasional thunder rumble",
             "tip": "Layer environmental sounds. Comma-separated."},
            {"id": "VisualStyle", "label": "Visual Style & Grading", "type": "text",
             "default": "desaturated, high contrast, film grain, teal-amber color grade, shallow DOF on Tyler",
             "tip": "Cinematic look and color treatment."},
        ],
        "template": (
            "{SceneSetup}. {Characters}. "
            "Camera: {CameraSequence}. "
            "Dialogue: {Dialogue} "
            "Ambient audio: {AmbientAudio}. "
            "Style: {VisualStyle}."
        )
    },
    {
        "name": "Wan Action/Sports Scene",
        "model": "wan",
        "description": "High-motion sports/action. 80-120 words. Wan 2.2+ handles complex movement excellently.",
        "guidance": "Wan 2.2's MoE architecture excels at sports and dynamic facial expressions. Be specific about motion mechanics.",
        "fields": [
            {"id": "Lighting", "label": "Lighting Quality", "type": "choice",
             "choices": [
                 "high contrast, hard light, side light",
                 "natural daylight, even lighting",
                 "dramatic spotlight",
                 "stadium lighting, bright"
             ],
             "default": "high contrast, hard light, side light",
             "tip": "Action often uses dramatic lighting."},
            {"id": "ShotFraming", "label": "Shot Size & Composition", "type": "text",
             "default": "medium shot, 24fps, daylight",
             "tip": "Frame the action to capture movement."},
            {"id": "Athlete", "label": "Athlete/Subject Detail", "type": "multiline",
             "default": "A sprinter with face distorted from exertion, facial muscles tight, jaw clenched, wearing lightweight athletic vest and shorts, professional running spikes",
             "tip": "Physical strain details. Wan 2.2 excels at facial expressions during action."},
            {"id": "ActionDynamics", "label": "Action Mechanics (be specific!)", "type": "multiline",
             "default": "Sprinting at incredible speed at the 100-meter finish line! Body leans forward at 45 degrees, head thrusts out, arms pump with maximum amplitude, one leg pushes off explosively generating power. Chest breaks through the finish tape.",
             "tip": "Describe biomechanics precisely. Use exclamation points for energy!"},
            {"id": "Environment", "label": "Environment & Context", "type": "text",
             "default": "Background shows blurred track, cheering audience, digital timer displaying time, bright finish tape",
             "tip": "Motion blur for speed. Include competitive context."},
            {"id": "AudioLayer", "label": "Audio (Wan 2.5 only)", "type": "text",
             "default": "pounding footsteps, heavy breathing, crowd roar, tape snapping",
             "tip": "Action-specific sounds. Leave blank for Wan 2.1/2.2."},
        ],
        "template": (
            "{Lighting}, {ShotFraming}. "
            "{Athlete} {ActionDynamics} "
            "{Environment}. "
            "Audio: {AudioLayer}"
        )
    },
]

# ==================== QWEN TEMPLATES ====================
QWEN_TEMPLATES = [
    {
        "name": "Qwen Single Image Edit",
        "model": "qwen",
        "description": "Edit one image: change background, add/remove objects, modify style. Natural language instructions.",
        "guidance": "Conversational instructions work best. Be specific about changes and preservation constraints.",
        "fields": [
            {"id": "SourceImage", "label": "Source Image Description", "type": "multiline",
             "default": "A person standing in a living room with white walls, grey couch, and wooden floor",
             "tip": "Describe what's currently in the image for context."},
            {"id": "EditInstruction", "label": "Main Edit Request", "type": "multiline",
             "default": "Change the background to a beach at sunset with golden sunlight and palm trees",
             "tip": "Clear, specific instruction. What should change?"},
            {"id": "Preserve", "label": "Preservation Constraints", "type": "text",
             "default": "Do not change the person, their clothing, pose, or facial features",
             "tip": "CRITICAL: explicitly state what must NOT change."},
            {"id": "LightingMatch", "label": "Lighting & Integration", "type": "text",
             "default": "Match lighting to sunset - warm golden light from right, soft shadows on person",
             "tip": "Lighting consistency is key for realism."},
            {"id": "StyleDetails", "label": "Additional Style Details", "type": "text",
             "default": "Maintain photorealistic quality, natural perspective, seamless integration",
             "tip": "Quality and consistency requirements."},
        ],
        "template": (
            "Source image: {SourceImage}\n\n"
            "Edit: {EditInstruction}\n"
            "Preserve: {Preserve}\n"
            "Lighting: {LightingMatch}\n"
            "Style: {StyleDetails}"
        )
    },
    {
        "name": "Qwen Multi-Image Composition",
        "model": "qwen",
        "description": "Combine 2-3 images seamlessly. Qwen's specialty: person+scene, person+product, person+person.",
        "guidance": "Describe spatial relationships clearly. Specify lighting direction and perspective consistency.",
        "fields": [
            {"id": "Image1", "label": "Image 1 Description", "type": "text",
             "default": "Person in business attire with neutral expression",
             "tip": "Primary subject (usually a person)."},
            {"id": "Image2", "label": "Image 2 Description", "type": "text",
             "default": "Modern office interior with desk and windows",
             "tip": "Scene, product, or second person."},
            {"id": "Image3", "label": "Image 3 (Optional)", "type": "text",
             "default": "",
             "tip": "Third image if needed. Leave blank for 2-image composition."},
            {"id": "SpatialArrangement", "label": "Spatial Composition", "type": "multiline",
             "default": "Place person from Image 1 sitting at the desk from Image 2, positioned on the left side of frame, looking toward the windows",
             "tip": "WHERE elements go, HOW they're positioned, WHAT they're doing."},
            {"id": "LightingConsistency", "label": "Lighting Integration", "type": "text",
             "default": "Soft window light from right illuminates person naturally, casting gentle shadows consistent with office environment",
             "tip": "Match light direction, quality, and temperature across all elements."},
            {"id": "PerspectiveScale", "label": "Perspective & Scale", "type": "text",
             "default": "Perspective-correct integration, person scaled naturally for desk height, camera angle eye-level",
             "tip": "Scale, perspective, and viewpoint must be consistent."},
        ],
        "template": (
            "Combine images:\n"
            "Image 1: {Image1}\n"
            "Image 2: {Image2}\n"
            "{Image3}\n\n"
            "Composition: {SpatialArrangement}\n"
            "Lighting: {LightingConsistency}\n"
            "Perspective: {PerspectiveScale}"
        )
    },
    {
        "name": "Qwen Text Replacement/Editing",
        "model": "qwen",
        "description": "Add, replace, or modify text in images. Qwen's top-rated text editing capability.",
        "guidance": "Quote exact text to replace. Works with English and Chinese. Specify font properties if modifying style.",
        "fields": [
            {"id": "ImageContext", "label": "Image Description", "type": "text",
             "default": "Product advertisement poster with 'SUMMER SALE' text at top in bold red letters",
             "tip": "Describe the image and current text location."},
            {"id": "OldText", "label": "Text to Replace (exact)", "type": "text",
             "default": "SUMMER SALE",
             "tip": "Exact current text. Use quotes for accuracy."},
            {"id": "NewText", "label": "New Text Content", "type": "text",
             "default": "WINTER CLEARANCE",
             "tip": "Replacement text. Can be different language (Chinese/English)."},
            {"id": "FontStyle", "label": "Font/Style Modifications (optional)", "type": "text",
             "default": "Keep same bold font, change color to blue",
             "tip": "Font type, color, size, effects. Optional - leave blank to match original."},
            {"id": "TextPosition", "label": "Position/Placement", "type": "text",
             "default": "Maintain current position at top center of image",
             "tip": "Where text should appear."},
        ],
        "template": (
            "Image: {ImageContext}\n\n"
            "Replace text '{OldText}' with '{NewText}'\n"
            "Font/style: {FontStyle}\n"
            "Position: {TextPosition}"
        )
    },
    {
        "name": "Qwen Character/IP Design",
        "model": "qwen",
        "description": "Create consistent character across multiple poses/settings. Identity preservation excellence.",
        "guidance": "Define character once, then vary pose/action/setting while preserving identity. Qwen excels at this.",
        "fields": [
            {"id": "CharacterCore", "label": "Core Character Description", "type": "multiline",
             "default": "A friendly cartoon bear with warm brown fur, wearing a blue wizard hat with stars, holding a wooden magic wand, expressive eyes, gentle smile",
             "tip": "Detailed character design. This stays CONSTANT across all variations."},
            {"id": "CurrentAction", "label": "Action/Pose for THIS Image", "type": "text",
             "default": "standing in front of an easel, painting with a brush, looking focused and happy",
             "tip": "What is the character doing in THIS specific image?"},
            {"id": "Setting", "label": "Setting/Environment", "type": "text",
             "default": "Art studio with colorful paintings on walls, wooden floor, natural window light streaming in",
             "tip": "Where is this scene taking place?"},
            {"id": "VisualStyle", "label": "Rendering Style", "type": "choice",
             "choices": [
                 "3D cartoon (Pixar-style)",
                 "2D flat illustration",
                 "Watercolor painting",
                 "Digital art",
                 "Felt/clay style",
                 "Pixel art",
                 "Anime style"
             ],
             "default": "3D cartoon (Pixar-style)",
             "tip": "Keep style consistent for character identity."},
            {"id": "IdentityLock", "label": "Identity Preservation", "type": "text",
             "default": "Maintain EXACT same facial features, fur texture, wizard hat design, wand appearance, and overall character proportions",
             "tip": "What features must be IDENTICAL to maintain character identity?"},
        ],
        "template": (
            "Character: {CharacterCore}\n"
            "Current action: {CurrentAction}\n"
            "Setting: {Setting}\n"
            "Style: {VisualStyle}\n"
            "Identity preservation: {IdentityLock}"
        )
    },
    {
        "name": "Qwen Product Photography Poster",
        "model": "qwen",
        "description": "Professional product marketing posters with text, backgrounds, and presentation elements.",
        "guidance": "Combine product with professional background, add marketing text. Clean, commercial-ready results.",
        "fields": [
            {"id": "Product", "label": "Product Description", "type": "text",
             "default": "White sneakers with blue accent stripes and red sole",
             "tip": "Clear product description with key visual details."},
            {"id": "Background", "label": "Background Type", "type": "choice",
             "choices": [
                 "plain white studio background",
                 "plain black background",
                 "gradient (specify colors below)",
                 "minimal geometric shapes",
                 "lifestyle scene (describe below)"
             ],
             "default": "plain white studio background",
             "tip": "Professional product photography backgrounds."},
            {"id": "BackgroundDetail", "label": "Background Details (if needed)", "type": "text",
             "default": "",
             "tip": "For gradients: specify colors. For lifestyle: describe scene."},
            {"id": "ProductLighting", "label": "Lighting Setup", "type": "text",
             "default": "Professional studio lighting, soft shadows, specular highlights on shoe surface, clean and even illumination",
             "tip": "Product photography requires controlled lighting."},
            {"id": "ProductText", "label": "Product Name/Main Text", "type": "text",
             "default": "CLOUDSTRIKE PRO",
             "tip": "Product name or main headline text."},
            {"id": "TextPlacement", "label": "Text Position", "type": "choice",
             "choices": [
                 "bottom center in bold typography",
                 "top center",
                 "bottom left corner",
                 "bottom right corner",
                 "floating near product"
             ],
             "default": "bottom center in bold typography",
             "tip": "Where to place product name."},
            {"id": "Tagline", "label": "Tagline/Additional Text (optional)", "type": "text",
             "default": "Performance Meets Style",
             "tip": "Secondary text, price, or marketing copy. Optional."},
        ],
        "template": (
            "Create professional product poster:\n"
            "Product: {Product}\n"
            "Background: {Background} {BackgroundDetail}\n"
            "Lighting: {ProductLighting}\n\n"
            "Add text: '{ProductText}' {TextPlacement}\n"
            "{Tagline}"
        )
    },
]

# ==================== NANO BANANA TEMPLATES ====================
NANO_TEMPLATES = [
    {
        "name": "Nano Banana Photography Style",
        "model": "nano",
        "description": "Professional photography with camera terminology. Gemini 2.5 Flash excels at photographic concepts.",
        "guidance": "Describe like instructing a professional photographer. Use camera settings and photographic terminology.",
        "fields": [
            {"id": "Subject", "label": "Subject & Context", "type": "multiline",
             "default": "An elderly Japanese ceramicist with deep sun-etched wrinkles and a warm, knowing smile, hands shaping clay on a pottery wheel",
             "tip": "Subject with personality, emotion, and action."},
            {"id": "Proximity", "label": "Camera Proximity", "type": "choice",
             "choices": [
                 "extreme close-up",
                 "close-up portrait",
                 "medium shot",
                 "wide shot",
                 "environmental portrait",
                 "aerial view"
             ],
             "default": "close-up portrait",
             "tip": "How close is the camera to subject?"},
            {"id": "Angle", "label": "Camera Angle", "type": "choice",
             "choices": [
                 "eye-level",
                 "from below (low angle)",
                 "from above (high angle)",
                 "bird's eye view",
                 "worm's eye view"
             ],
             "default": "eye-level",
             "tip": "Shooting angle affects perspective and power dynamics."},
            {"id": "Lens", "label": "Lens Specification", "type": "choice",
             "choices": [
                 "35mm lens",
                 "50mm lens",
                 "85mm portrait lens",
                 "24mm wide angle",
                 "100mm macro lens",
                 "fisheye lens"
             ],
             "default": "35mm lens",
             "tip": "Lens type affects depth, compression, and field of view."},
            {"id": "Lighting", "label": "Lighting Style", "type": "choice",
             "choices": [
                 "natural window lighting",
                 "soft diffused studio light",
                 "dramatic side lighting",
                 "golden hour sunlight",
                 "harsh overhead light",
                 "rim/back lighting"
             ],
             "default": "natural window lighting",
             "tip": "Lighting defines mood and quality."},
            {"id": "CameraSettings", "label": "Camera Settings & Effects", "type": "text",
             "default": "shallow depth of field, soft bokeh background, professional photography",
             "tip": "DOF, bokeh, motion blur, sharpness, focus."},
            {"id": "Mood", "label": "Mood/Atmosphere", "type": "text",
             "default": "serene and masterful, contemplative",
             "tip": "Overall emotional tone."},
            {"id": "Quality", "label": "Quality Descriptors", "type": "text",
             "default": "high-quality, professional, award-winning photography, DSLR camera",
             "tip": "Quality modifiers improve generation."},
        ],
        "template": (
            "A photorealistic {Proximity} of {Subject}. "
            "Shot with {Lens}, {Angle}. "
            "{Lighting}. "
            "{CameraSettings}. "
            "The overall mood is {Mood}. "
            "{Quality}"
        )
    },
    {
        "name": "Nano Banana Character Consistency",
        "model": "nano",
        "description": "Maintain same character across multiple images. Nano Banana's top feature.",
        "guidance": "First image creates character. Use EXACT same character description in all subsequent generations for consistency.",
        "fields": [
            {"id": "CharacterBase", "label": "Character Description (KEEP CONSISTENT)", "type": "multiline",
             "default": "A young woman with shoulder-length brown hair, bright green eyes, fair skin with light freckles, wearing a red hoodie and blue jeans, friendly warm smile",
             "tip": "Detailed character design. Copy-paste this EXACT description for all variations."},
            {"id": "NewAction", "label": "New Action/Pose", "type": "text",
             "default": "sitting at a cafe table with a laptop, looking thoughtful while typing",
             "tip": "What is the character doing in THIS image?"},
            {"id": "NewSetting", "label": "New Location/Environment", "type": "text",
             "default": "cozy coffee shop interior with warm lighting, wooden tables, bookshelves in background",
             "tip": "Where is this scene happening?"},
            {"id": "OutfitChange", "label": "Outfit (change or keep same)", "type": "text",
             "default": "Keep the same red hoodie and blue jeans",
             "tip": "Explicitly state if outfit changes or stays same."},
            {"id": "Framing", "label": "Camera Framing", "type": "text",
             "default": "medium shot from slightly above, showing upper body and laptop",
             "tip": "How is the shot composed?"},
            {"id": "Preservation", "label": "Feature Preservation", "type": "text",
             "default": "maintaining exact same facial features, hair style and color, eye color, skin tone, and overall appearance",
             "tip": "CRITICAL: what facial features must stay identical?"},
        ],
        "template": (
            "The same character: {CharacterBase}. "
            "Now {NewAction} in {NewSetting}. "
            "{OutfitChange}. "
            "{Framing}. "
            "{Preservation}"
        )
    },
    {
        "name": "Nano Banana Iterative Editing",
        "model": "nano",
        "description": "Multi-turn conversational editing. Make specific changes while preserving other elements.",
        "guidance": "Nano Banana remembers conversation context. Build edits incrementally. One change at a time works best.",
        "fields": [
            {"id": "CurrentImage", "label": "Current Image State", "type": "multiline",
             "default": "A modern living room with white walls, grey fabric sofa, wooden floor, and a window with natural light",
             "tip": "Describe the image as it currently exists."},
            {"id": "Change", "label": "Requested Change", "type": "multiline",
             "default": "Add a floor-to-ceiling bookshelf on the left wall, filled with colorful books and decorative items",
             "tip": "What to add, remove, or modify. Be specific and clear."},
            {"id": "Preserve", "label": "What Stays the Same", "type": "text",
             "default": "Keep the sofa, floor, window, and wall color exactly the same",
             "tip": "Explicitly state what should NOT change."},
            {"id": "Integration", "label": "Integration & Style Matching", "type": "text",
             "default": "Bookshelf should match the modern minimalist aesthetic, with natural lighting consistent with the window",
             "tip": "How new elements should fit with existing style."},
        ],
        "template": (
            "Current image: {CurrentImage}\n\n"
            "Change: {Change}\n"
            "Preserve: {Preserve}\n"
            "Integration: {Integration}"
        )
    },
    {
        "name": "Nano Banana Style Transform",
        "model": "nano",
        "description": "Transform photo into different artistic styles. Art/illustration generation.",
        "guidance": "Convert existing image to artistic style. Specify medium and artistic approach clearly.",
        "fields": [
            {"id": "SourceImage", "label": "Source Image Description", "type": "multiline",
             "default": "A portrait photograph of a person in casual clothing with neutral background",
             "tip": "Describe the starting image."},
            {"id": "TargetStyle", "label": "Target Art Style", "type": "choice",
             "choices": [
                 "oil painting",
                 "watercolor painting",
                 "pencil sketch/drawing",
                 "digital illustration",
                 "anime/manga style",
                 "pop art",
                 "impressionist painting",
                 "cartoon/comic book style",
                 "pixel art"
             ],
             "default": "oil painting",
             "tip": "Which artistic style to apply?"},
            {"id": "StyleDetails", "label": "Style Specifics", "type": "text",
             "default": "in the style of Van Gogh with visible brushstrokes and vibrant colors",
             "tip": "Reference artists, techniques, or specific characteristics."},
            {"id": "Preserve", "label": "Elements to Preserve", "type": "text",
             "default": "Maintain the person's facial features, pose, and overall composition",
             "tip": "What from the original should stay recognizable?"},
            {"id": "Medium", "label": "Medium/Materials", "type": "text",
             "default": "thick oil paint on canvas with textured brushwork",
             "tip": "Describe the artistic medium and texture."},
        ],
        "template": (
            "Transform this image: {SourceImage}\n\n"
            "Into: {TargetStyle}\n"
            "Style details: {StyleDetails}\n"
            "Using medium: {Medium}\n"
            "Preserve: {Preserve}"
        )
    },
    {
        "name": "Nano Banana Figurine/Collectible",
        "model": "nano",
        "description": "Transform photo into collectible figurine. Viral Nano Banana trend.",
        "guidance": "Popular use case: turn photos into toy figurines with packaging. Fun and creative transformations.",
        "fields": [
            {"id": "SourcePhoto", "label": "Source Photo Description", "type": "text",
             "default": "A person in casual outfit standing and smiling at camera",
             "tip": "Describe the original photo/person."},
            {"id": "FigurineStyle", "label": "Figurine Style", "type": "choice",
             "choices": [
                 "realistic detailed collectible",
                 "chibi/cute style",
                 "action figure style",
                 "funko pop style",
                 "anime figure style"
             ],
             "default": "realistic detailed collectible",
             "tip": "What type of figurine?"},
            {"id": "Packaging", "label": "Include Packaging", "type": "choice",
             "choices": [
                 "yes - with product box showing character image",
                 "yes - with blister pack and cardboard",
                 "no - just the figurine"
             ],
             "default": "yes - with product box showing character image",
             "tip": "Packaging makes it look like real product."},
            {"id": "Extras", "label": "Additional Elements", "type": "text",
             "default": "Round display base, computer screen showing 3D modeling software in background",
             "tip": "Base, accessories, scene elements (computer, workspace, etc)."},
        ],
        "template": (
            "Transform photo: {SourcePhoto}\n\n"
            "Into a {FigurineStyle} collectible figurine. "
            "{Packaging}. "
            "Include: {Extras}. "
            "Realistic product photography quality."
        )
    },
]

# ==================== COMBINED TEMPLATES ====================
ALL_TEMPLATES = SORA_TEMPLATES + WAN_TEMPLATES + QWEN_TEMPLATES + NANO_TEMPLATES

# Helper function to get templates by model
def get_templates_by_model(model_name):
    """
    Get all templates for a specific model.
    
    Args:
        model_name (str): 'sora', 'wan', 'qwen', or 'nano'
    
    Returns:
        list: Templates for the specified model
    """
    return [t for t in ALL_TEMPLATES if t.get('model') == model_name]

# Template validation function
def validate_template(template):
    """
    Validate template structure.
    
    Args:
        template (dict): Template to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_keys = ['name', 'model', 'description', 'guidance', 'fields', 'template']
    
    for key in required_keys:
        if key not in template:
            return False, f"Missing required key: {key}"
    
    if not isinstance(template['fields'], list):
        return False, "Fields must be a list"
    
    for field in template['fields']:
        required_field_keys = ['id', 'label', 'type']
        for key in required_field_keys:
            if key not in field:
                return False, f"Field missing required key: {key}"
    
    return True, "Valid"

# Validate all templates on import
def validate_all_templates():
    """Validate all templates and print any errors."""
    errors = []
    for template in ALL_TEMPLATES:
        is_valid, message = validate_template(template)
        if not is_valid:
            errors.append(f"Template '{template.get('name', 'UNKNOWN')}': {message}")
    
    if errors:
        print("⚠️  Template Validation Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"✅ All {len(ALL_TEMPLATES)} templates validated successfully")

# Run validation when module is imported
if __name__ != '__main__':
    validate_all_templates()