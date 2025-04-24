document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const brandAnalysisForm = document.getElementById('brandAnalysisForm');
    const analyzeButton = document.getElementById('analyzeButton');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const loadingContainer = document.getElementById('loadingContainer');
    const loadingMessage = document.getElementById('loadingMessage');
    const resultsContainer = document.getElementById('resultsContainer');
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    
    // Result elements
    const personaName = document.getElementById('personaName');
    const colorPalette = document.getElementById('colorPalette');
    const toneKeywords = document.getElementById('toneKeywords');
    const styleKeywords = document.getElementById('styleKeywords');
    const contentThemes = document.getElementById('contentThemes');
    const voiceDescription = document.getElementById('voiceDescription');
    const saveToProfileButton = document.getElementById('saveToProfileButton');
    const exportJsonButton = document.getElementById('exportJsonButton');
    
    // Current persona data
    let currentPersona = null;
    
    // Form submission handler
    brandAnalysisForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        setLoading(true);
        
        // Get form data
        const formData = new FormData(brandAnalysisForm);
        const brand_name = formData.get('brand_name');
        const industry = formData.get('industry');
        const pinterest_board = formData.get('pinterest_board');
        const keywords = formData.get('keywords') ? formData.get('keywords').split(',').map(k => k.trim()) : [];
        
        // Prepare request payload
        const payload = {
            brand_name,
            industry,
            pinterest_board,
            keywords
        };
        
        try {
            // Upload assets if provided
            const assetFiles = formData.getAll('assets');
            if (assetFiles && assetFiles.length > 0 && assetFiles[0].size > 0) {
                loadingMessage.textContent = 'Uploading assets...';
                
                const assetFormData = new FormData();
                assetFiles.forEach(file => {
                    assetFormData.append('files', file);
                });
                
                const assetResponse = await fetch('/analyze/brand/upload', {
                    method: 'POST',
                    body: assetFormData
                });
                
                if (!assetResponse.ok) {
                    throw new Error('Failed to upload assets');
                }
                
                const assetUrls = await assetResponse.json();
                payload.assets = assetUrls;
            }
            
            // Call the brand analysis API
            loadingMessage.textContent = 'Analyzing Pinterest board...';
            
            const response = await fetch('/analyze/brand/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to analyze brand');
            }
            
            // Process the response
            const persona = await response.json();
            displayResults(persona);
            currentPersona = persona;
            
        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
        }
    });
    
    // Display the analysis results
    function displayResults(persona) {
        // Hide empty state and show results
        emptyStateContainer.classList.add('d-none');
        resultsContainer.classList.remove('d-none');
        
        // Populate result fields
        personaName.textContent = persona.name;
        
        // Display color palette
        colorPalette.innerHTML = '';
        persona.colors.forEach(color => {
            const swatch = document.createElement('div');
            swatch.className = 'color-swatch';
            swatch.style.backgroundColor = color;
            
            const colorCode = document.createElement('div');
            colorCode.className = 'color-code';
            colorCode.textContent = color;
            swatch.appendChild(colorCode);
            
            colorPalette.appendChild(swatch);
        });
        
        // Display keywords as tags
        toneKeywords.innerHTML = '';
        persona.tone_keywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            toneKeywords.appendChild(tag);
        });
        
        styleKeywords.innerHTML = '';
        persona.style_keywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            styleKeywords.appendChild(tag);
        });
        
        contentThemes.innerHTML = '';
        persona.content_themes.forEach(theme => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = theme;
            contentThemes.appendChild(tag);
        });
        
        // Display voice description
        voiceDescription.textContent = persona.voice_description;
    }
    
    // Set loading state
    function setLoading(isLoading) {
        if (isLoading) {
            analyzeButton.disabled = true;
            loadingSpinner.classList.remove('d-none');
            loadingContainer.classList.remove('d-none');
            emptyStateContainer.classList.add('d-none');
            resultsContainer.classList.add('d-none');
            errorContainer.classList.add('d-none');
        } else {
            analyzeButton.disabled = false;
            loadingSpinner.classList.add('d-none');
            loadingContainer.classList.add('d-none');
        }
    }
    
    // Show error message
    function showError(message) {
        errorContainer.classList.remove('d-none');
        errorMessage.textContent = message;
        emptyStateContainer.classList.add('d-none');
        resultsContainer.classList.add('d-none');
    }
    
    // Export JSON button handler
    exportJsonButton.addEventListener('click', function() {
        if (!currentPersona) return;
        
        const dataStr = JSON.stringify(currentPersona, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `${currentPersona.brand_name.replace(/\s+/g, '_')}_persona.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    });
    
    // Save to Profile button handler
    saveToProfileButton.addEventListener('click', function() {
        if (!currentPersona) return;
        
        // In a real implementation, this would save to a user profile or pipeline
        alert('Persona saved to profile! (This is a mock implementation)');
        
        // Redirect to pipeline page or show confirmation modal
        // window.location.href = '/pipelines?personaId=' + currentPersona.id;
    });
});
