// Global state
let templates = [];
let currentTemplate = null;
let fieldValues = {};
let availableModels = [];

// DOM Elements
const templateSelect = document.getElementById('templateSelect');
const templateDescription = document.getElementById('templateDescription');
const fieldsContainer = document.getElementById('fieldsContainer');
const outputText = document.getElementById('outputText');
const includeLabels = document.getElementById('includeLabels');

// AI Elements
const toggleAI = document.getElementById('toggleAI');
const aiContent = document.getElementById('aiContent');
const userPrompt = document.getElementById('userPrompt');
const assistBtn = document.getElementById('assistBtn');
const aiStatus = document.getElementById('aiStatus');
const ollamaStatus = document.getElementById('ollamaStatus');
const modelSelect = document.getElementById('modelSelect');

// Buttons
const generateBtn = document.getElementById('generateBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

// Initialize
async function init() {
    await loadTemplates();
    await checkOllamaStatus();
    setupEventListeners();
}

// Load templates from API
async function loadTemplates() {
    try {
        const response = await fetch('/api/templates');
        templates = await response.json();
        populateTemplateSelect();
    } catch (error) {
        console.error('Failed to load templates:', error);
        showNotification('Failed to load templates', 'error');
    }
}

// Populate template dropdown
function populateTemplateSelect() {
    templateSelect.innerHTML = '<option value="">Select a protocol...</option>';
    templates.forEach((template, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = template.name;
        templateSelect.appendChild(option);
    });
}

// Check if Ollama is running and load models
async function checkOllamaStatus() {
    console.log('[DEBUG] Checking Ollama status...');
    try {
        console.log('[DEBUG] Fetching /api/ollama_models');
        const response = await fetch('/api/ollama_models');
        console.log('[DEBUG] Response status:', response.status);
        const data = await response.json();
        console.log('[DEBUG] Response data:', data);
        
        if (response.ok && data.status === 'online') {
            availableModels = data.models || [];
            console.log('[DEBUG] Found models:', availableModels);
            
            ollamaStatus.textContent = `✓ OLLAMA ONLINE (${availableModels.length} models)`;
            ollamaStatus.classList.add('online');
            
            // Populate model selector
            populateModelSelect();
        } else {
            console.log('[DEBUG] Ollama offline or error:', data);
            ollamaStatus.textContent = '⚠ OLLAMA OFFLINE';
            ollamaStatus.classList.remove('online');
            modelSelect.innerHTML = '<option value="">Ollama not running - Start with: ollama serve</option>';
        }
    } catch (error) {
        console.error('[ERROR] Failed to check Ollama status:', error);
        ollamaStatus.textContent = '⚠ OLLAMA OFFLINE';
        ollamaStatus.classList.remove('online');
        modelSelect.innerHTML = '<option value="">Ollama not running - Start with: ollama serve</option>';
    }
}

// Populate model selector
function populateModelSelect() {
    if (availableModels.length === 0) {
        modelSelect.innerHTML = '<option value="">No models found</option>';
        return;
    }
    
    modelSelect.innerHTML = '';
    availableModels.forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        option.textContent = model;
        modelSelect.appendChild(option);
    });
    
    // Default to llama3.2 if available
    const defaultModel = availableModels.find(m => m.includes('llama3.2')) || availableModels[0];
    modelSelect.value = defaultModel;
}

// Setup event listeners
function setupEventListeners() {
    templateSelect.addEventListener('change', onTemplateChange);
    toggleAI.addEventListener('click', toggleAISection);
    assistBtn.addEventListener('click', engageAIAssistant);
    generateBtn.addEventListener('click', generatePrompt);
    clearBtn.addEventListener('click', clearFields);
    copyBtn.addEventListener('click', copyToClipboard);
    downloadBtn.addEventListener('click', downloadPrompt);
}

// Template change handler
function onTemplateChange() {
    const index = templateSelect.value;
    if (index === '') {
        currentTemplate = null;
        templateDescription.textContent = 'Awaiting protocol selection...';
        fieldsContainer.innerHTML = '<p class="placeholder-text">Select a protocol to configure parameters...</p>';
        return;
    }
    
    currentTemplate = templates[index];
    templateDescription.textContent = currentTemplate.description;
    renderFields();
}

// Render form fields
function renderFields() {
    fieldsContainer.innerHTML = '';
    fieldValues = {};
    
    currentTemplate.fields.forEach(field => {
        const fieldGroup = document.createElement('div');
        fieldGroup.className = 'field-group';
        
        const label = document.createElement('label');
        label.className = 'field-label';
        label.textContent = field.label;
        fieldGroup.appendChild(label);
        
        let input;
        switch (field.type) {
            case 'multiline':
                input = document.createElement('textarea');
                input.className = 'field-textarea';
                input.value = field.default || '';
                break;
            case 'choice':
                input = document.createElement('select');
                input.className = 'field-select';
                field.choices.forEach(choice => {
                    const option = document.createElement('option');
                    option.value = choice;
                    option.textContent = choice;
                    input.appendChild(option);
                });
                input.value = field.default || '';
                break;
            default:
                input = document.createElement('input');
                input.className = 'field-input';
                input.type = field.type === 'int' ? 'number' : 'text';
                input.value = field.default || '';
        }
        
        input.id = `field_${field.id}`;
        input.dataset.fieldId = field.id;
        input.addEventListener('input', () => {
            fieldValues[field.id] = input.value;
        });
        
        fieldGroup.appendChild(input);
        fieldsContainer.appendChild(fieldGroup);
        
        fieldValues[field.id] = input.value;
    });
}

// Toggle AI section
function toggleAISection() {
    const isHidden = aiContent.style.display === 'none';
    aiContent.style.display = isHidden ? 'block' : 'none';
    toggleAI.textContent = isHidden ? 'COLLAPSE' : 'EXPAND';
}

// Engage AI Assistant
async function engageAIAssistant() {
    if (!currentTemplate) {
        showAIStatus('Please select a protocol first', 'error');
        return;
    }
    
    const prompt = userPrompt.value.trim();
    if (!prompt) {
        showAIStatus('Please describe your video idea', 'error');
        return;
    }
    
    const selectedModel = modelSelect.value;
    if (!selectedModel) {
        showAIStatus('Please select an Ollama model', 'error');
        return;
    }
    
    showAIStatus(`Consulting ${selectedModel}...`, 'loading');
    assistBtn.disabled = true;
    assistBtn.innerHTML = '<span class="btn-icon loading">⚙</span> PROCESSING...';
    
    try {
        const response = await fetch('/api/ollama_assist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_prompt: prompt,
                template: currentTemplate.name,
                current_values: fieldValues,
                model: selectedModel
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.suggestions) {
            applyAISuggestions(data.suggestions);
            showAIStatus(`AI assistance from ${selectedModel} applied successfully! Review and adjust as needed.`, 'success');
        } else {
            showAIStatus(data.error || 'AI assistance failed', 'error');
        }
    } catch (error) {
        showAIStatus('Could not connect to Ollama. Make sure it\'s running!', 'error');
    } finally {
        assistBtn.disabled = false;
        assistBtn.innerHTML = '<span class="btn-icon">🤖</span> ENGAGE AI ASSISTANT';
    }
}

// Apply AI suggestions to fields
function applyAISuggestions(suggestions) {
    Object.entries(suggestions).forEach(([fieldId, value]) => {
        const input = document.querySelector(`[data-field-id="${fieldId}"]`);
        if (input && value) {
            input.value = value;
            fieldValues[fieldId] = value;
        }
    });
}

// Show AI status message
function showAIStatus(message, type) {
    aiStatus.textContent = message;
    aiStatus.className = `ai-status ${type}`;
}

// Generate prompt
async function generatePrompt() {
    if (!currentTemplate) {
        showNotification('Please select a protocol first', 'error');
        return;
    }
    
    // Collect current values
    const values = {};
    currentTemplate.fields.forEach(field => {
        const input = document.querySelector(`[data-field-id="${field.id}"]`);
        values[field.id] = input ? input.value : '';
    });
    
    try {
        const response = await fetch('/api/generate_prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                template: currentTemplate.name,
                values: values,
                include_labels: includeLabels.checked
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            outputText.value = data.prompt;
            showNotification('Prompt generated successfully!', 'success');
        } else {
            showNotification(data.error || 'Generation failed', 'error');
        }
    } catch (error) {
        showNotification('Failed to generate prompt', 'error');
    }
}

// Clear fields
function clearFields() {
    fieldsContainer.querySelectorAll('input, textarea, select').forEach(input => {
        if (input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        } else {
            input.value = '';
        }
    });
    outputText.value = '';
    userPrompt.value = '';
    fieldValues = {};
    showNotification('All fields cleared', 'success');
}

// Copy to clipboard
async function copyToClipboard() {
    const text = outputText.value;
    if (!text.trim()) {
        showNotification('Nothing to copy yet', 'error');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (error) {
        showNotification('Failed to copy', 'error');
    }
}

// Download prompt as .txt
function downloadPrompt() {
    const text = outputText.value;
    if (!text.trim()) {
        showNotification('Nothing to download yet', 'error');
        return;
    }
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sora_prompt_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showNotification('Prompt downloaded!', 'success');
}

// Show notification (simple console log for now)
function showNotification(message, type) {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // You could implement a toast notification system here
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);