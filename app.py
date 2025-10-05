#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sora Prompt Maker - Web Edition (Production Version)
Multi-Model Support: SORA, WAN, QWEN, NANO BANANA

Templates are imported from prompt_templates.py for better organization
"""
from flask import Flask, render_template, jsonify, request
import json
import requests
from pathlib import Path
import logging

# Import templates from separate module
from prompt_templates import ALL_TEMPLATES, get_templates_by_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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
    "wan_specifics": "Use Wan's prompt extension feature for quality. Focus on ONE action per 5-second clip. Wan 2.5 excels at audio-video sync.",
    "qwen_specifics": "Natural language works best. Explicitly preserve what shouldn't change. Excellent for multi-image composition (2-3 images).",
    "nano_specifics": "Photography terminology improves results. Character consistency is top feature. Iterative editing via conversation works well.",
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
    """Return all available prompt templates"""
    try:
        logger.info(f"Loaded {len(ALL_TEMPLATES)} templates total")
        return jsonify(ALL_TEMPLATES)
    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        return jsonify({'error': 'Failed to fetch templates'}), 500

@app.route('/api/templates/<model>')
def get_model_templates(model):
    """Return templates for a specific model"""
    try:
        templates = get_templates_by_model(model)
        logger.info(f"Loaded {len(templates)} templates for model: {model}")
        return jsonify(templates)
    except Exception as e:
        logger.error(f"Error fetching templates for {model}: {e}")
        return jsonify({'error': f'Failed to fetch templates for {model}'}), 500

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
            logger.info(f"Found {len(models)} Ollama models")
            return jsonify({'models': models, 'status': 'online'})
        return jsonify({'error': 'Failed to fetch models', 'status': 'error'}), 500
    except requests.exceptions.ConnectionError:
        logger.warning("Ollama not running")
        return jsonify({'error': 'Ollama not running', 'status': 'offline'}), 503
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
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
        
        # Find template by name
        template = next((t for t in ALL_TEMPLATES if t['name'] == template_name), None)
        if not template:
            logger.error(f"Template not found: {template_name}")
            return jsonify({'error': 'Template not found'}), 404
        
        # Generate prompt from template
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
        
        logger.info(f"Generated prompt: {word_count} words for {template_name}")
        
        return jsonify({
            'prompt': rendered,
            'word_count': word_count,
            'optimal': 50 <= word_count <= 120
        })
    except KeyError as e:
        logger.error(f"Missing field in template: {e}")
        return jsonify({'error': f'Missing required field: {e}'}), 400
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        return jsonify({'error': 'Failed to generate prompt'}), 500

@app.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    """Analyze uploaded image with vision model and generate video concept description"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        image_data = data.get('image', None)
        model = data.get('model', 'llama3.2-vision')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Check if model is vision-capable
        is_vision_model = any(keyword in model.lower() for keyword in ['vision', 'llava', 'moondream'])
        if not is_vision_model:
            return jsonify({'error': 'Selected model is not vision-capable'}), 400
        
        logger.info(f"Analyzing image with vision model: {model}")
        
        # Extract base64 image data
        try:
            img_base64 = image_data.get('data', '')
            if ',' in img_base64:
                img_base64 = img_base64.split(',', 1)[1]
        except Exception as e:
            logger.error(f"Error processing image data: {e}")
            return jsonify({'error': f'Image processing error: {str(e)}'}), 500
        
        # Build vision prompt for concept generation
        vision_prompt = """Analyze this image and create a detailed video concept description for AI video generation.

Your task:
1. Describe what you see in the image in detail
2. Imagine this as a starting point or inspiration for a video
3. Write a 2-3 sentence video concept that captures the essence, mood, and visual elements

Focus on:
- Main subject and their appearance/characteristics
- Setting, environment, atmosphere
- Lighting, time of day, weather
- Mood and emotional tone
- Potential action or movement

Write naturally as if describing a video you want to create. Be specific and vivid.

Output ONLY the video concept description, no preamble or explanation."""

        # Build request to Ollama
        request_payload = {
            'model': model,
            'prompt': vision_prompt,
            'images': [img_base64],
            'stream': False,
            'options': {
                'temperature': 0.7,  # Slightly creative but focused
                'top_p': 0.9,
                'top_k': 40
            }
        }
        
        logger.info(f"Sending vision analysis request to Ollama")
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=request_payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            concept = result.get('response', '').strip()
            
            logger.info(f"Vision analysis complete: {len(concept)} chars")
            return jsonify({'concept': concept})
        else:
            logger.error(f"Ollama request failed with status {response.status_code}")
            return jsonify({
                'error': f'Ollama request failed: HTTP {response.status_code}',
                'details': response.text
            }), 500
            
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to Ollama")
        return jsonify({'error': 'Could not connect to Ollama'}), 503
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        return jsonify({'error': 'Vision analysis timed out'}), 504
    except Exception as e:
        logger.error(f"Unexpected error in image analysis: {e}", exc_info=True)
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/ollama_assist', methods=['POST'])
def ollama_assist():
    """AI-assisted prompt generation via Ollama - fills template fields from concept description"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_prompt = data.get('user_prompt', '').strip()
        template_name = data.get('template')
        current_values = data.get('current_values', {})
        model = data.get('model', 'llama3.2')
        
        # Generation control parameters
        temperature = data.get('temperature', 1.0)
        top_p = data.get('top_p', 0.9)
        top_k = data.get('top_k', 40)
        seed = data.get('seed', None)
        
        if not template_name:
            return jsonify({'error': 'Template name required'}), 400
        
        if not user_prompt:
            return jsonify({'error': 'Concept description required'}), 400
        
        # Find template
        template = next((t for t in ALL_TEMPLATES if t['name'] == template_name), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # Build field descriptions
        field_descriptions = '\n'.join([
            f"- {f['id']}: {f['label']}"
            + (f" (tip: {f['tip']})" if 'tip' in f else "")
            for f in template['fields']
        ])
        
        # Build enhanced system prompt with STRONG emphasis on user input
        system_prompt = f"""You are an expert prompt engineer for {template.get('model', 'AI').upper()} video/image generation.

CRITICAL INSTRUCTION: You MUST base your suggestions ENTIRELY on the user's concept description. DO NOT use template defaults.

TEMPLATE: {template_name}
TEMPLATE GUIDANCE: {template.get('guidance', '')}

FIELDS TO FILL:
{field_descriptions}

USER'S CONCEPT/DESCRIPTION: "{user_prompt}"

TASK:
1. READ the user's concept carefully
2. For EACH field, suggest a value that matches the user's concept
3. If user concept is vague, infer reasonable details that fit their description
4. DO NOT copy template default values
5. Output ONLY valid JSON with field IDs as keys

Example:
If user says "A tank rolling through a desert"
- Subject should be about a TANK, not a person
- Setting should be DESERT
- Action should be ROLLING/MOVING
etc.

Output format (JSON only, no explanations):
{{"field_id": "value based on user's concept", ...}}"""

        logger.info(f"User prompt: '{user_prompt}'")
        
        # Build options dictionary with generation parameters
        options = {
            'temperature': temperature,
            'top_p': top_p,
            'top_k': top_k,
        }
        
        # Only include seed if provided
        if seed is not None:
            try:
                options['seed'] = int(seed)
            except (ValueError, TypeError):
                pass
        
        logger.info(f"Ollama request: temp={temperature}, top_p={top_p}, top_k={top_k}, seed={seed}")
        
        # Build request payload
        request_payload = {
            'model': model,
            'prompt': system_prompt,
            'stream': False,
            'options': options
        }
        
        # Make request to Ollama
        logger.info(f"Sending request to Ollama with model: {model}")
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=request_payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', '')
            
            logger.info(f"LLM raw response: {llm_response[:200]}...")
            
            # Try to extract JSON from response
            try:
                # Find JSON in response
                start = llm_response.find('{')
                end = llm_response.rfind('}') + 1
                
                if start != -1 and end > start:
                    json_str = llm_response[start:end]
                    suggestions = json.loads(json_str)
                    
                    logger.info(f"Successfully parsed {len(suggestions)} field suggestions")
                    return jsonify({'suggestions': suggestions})
                else:
                    logger.error("No JSON found in LLM response")
                    return jsonify({
                        'error': 'LLM did not return valid JSON',
                        'raw': llm_response
                    }), 500
                    
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                logger.error(f"Attempted to parse: {llm_response[start:end] if start != -1 else 'No JSON found'}")
                return jsonify({
                    'error': f'Could not parse LLM response as JSON: {str(e)}',
                    'raw': llm_response
                }), 500
        else:
            logger.error(f"Ollama request failed with status {response.status_code}")
            return jsonify({
                'error': f'Ollama request failed: HTTP {response.status_code}',
                'details': response.text
            }), 500
            
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to Ollama")
        return jsonify({'error': 'Could not connect to Ollama. Make sure Ollama is running on localhost:11434'}), 503
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        return jsonify({'error': 'Ollama request timed out. Try a simpler prompt.'}), 504
    except Exception as e:
        logger.error(f"Unexpected error in Ollama assist: {e}", exc_info=True)
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

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
        logger.info(f"Loaded {len(ALL_TEMPLATES)} templates from prompt_templates.py")
        
        # Log template counts by model
        for model in ['sora', 'wan', 'qwen', 'nano']:
            count = len(get_templates_by_model(model))
            logger.info(f"  - {model.upper()}: {count} templates")
    except Exception as e:
        logger.error(f"Failed to initialize directories: {e}")
        raise

if __name__ == '__main__':
    try:
        initialize_app()
        
        print("\n" + "="*70)
        print("STUDIO 42 PROMPT CRAFTER - PRODUCTION MODE")
        print("="*70)
        print("\nMulti-Model AI Prompt Generation System:")
        print("  ✓ SORA - OpenAI's cinematic video generation")
        print("  ✓ WAN - Alibaba's video models (2.1, 2.2, 2.5)")
        print("  ✓ QWEN - Image editing with multi-image composition")
        print("  ✓ NANO BANANA - Gemini 2.5 Flash image generation")
        print(f"\nTotal Templates: {len(ALL_TEMPLATES)}")
        for model in ['sora', 'wan', 'qwen', 'nano']:
            count = len(get_templates_by_model(model))
            print(f"  - {model.upper()}: {count} templates")
        print("\nServer running at: http://127.0.0.1:5000")
        print("(Local access only - Production WSGI server)")
        print("\nOptional: Start Ollama for AI-assisted prompt generation")
        print("   ollama run llama3.2-vision")
        print("="*70 + "\n")
        
        # Use Waitress production WSGI server
        from waitress import serve
        logger.info("Starting production server with Waitress")
        serve(app, host='127.0.0.1', port=5000, threads=4, channel_timeout=120)
        
    except ImportError:
        logger.error("Waitress not installed. Install with: pip install waitress")
        print("\n[ERROR] Production server (Waitress) not installed.")
        print("Install it with: pip install waitress")
        print("\nFalling back to development server (not recommended)...\n")
        app.run(host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        print(f"\n[CRITICAL ERROR] Application failed to start: {e}\n")
        exit(1)