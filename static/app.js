// Character counter for textarea
document.getElementById('inputText').addEventListener('input', function() {
    const text = this.value;
    const charCount = document.getElementById('charCount');
    charCount.textContent = text.length;
    
    if (text.length > 1800) {
        charCount.classList.add('text-warning');
    } else if (text.length === 2000) {
        charCount.classList.add('text-danger');
        charCount.classList.remove('text-warning');
    } else {
        charCount.classList.remove('text-warning', 'text-danger');
    }
});

// Range sliders
document.getElementById('maxLength').addEventListener('input', function() {
    document.getElementById('lengthValue').textContent = this.value;
});

document.getElementById('temperature').addEventListener('input', function() {
    document.getElementById('tempValue').textContent = this.value;
});

// Form submission
document.getElementById('paraphraseForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const inputText = document.getElementById('inputText').value.trim();
    const maxLength = parseInt(document.getElementById('maxLength').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    
    if (!inputText) {
        showError('Please enter some text to paraphrase.');
        return;
    }
    
    // Show loading state
    const submitBtn = document.getElementById('paraphraseBtn');
    const spinner = document.getElementById('loadingSpinner');
    const resultCard = document.getElementById('resultCard');
    const errorAlert = document.getElementById('errorAlert');
    
    submitBtn.disabled = true;
    spinner.classList.remove('d-none');
    resultCard.classList.add('d-none');
    errorAlert.classList.add('d-none');
    
    try {
        const response = await fetch('/api/paraphrase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                max_length: maxLength,
                temperature: temperature
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'An error occurred');
        }
        
        if (data.success) {
            showResult(data);
        } else {
            throw new Error(data.message || 'Failed to paraphrase text');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        // Hide loading state
        submitBtn.disabled = false;
        spinner.classList.add('d-none');
    }
});

function showResult(data) {
    const resultCard = document.getElementById('resultCard');
    const originalText = document.getElementById('originalText');
    const paraphrasedText = document.getElementById('paraphrasedText');
    const processingTime = document.getElementById('processingTime');
    
    originalText.textContent = data.original_text;
    paraphrasedText.textContent = data.paraphrased_text;
    processingTime.textContent = data.processing_time_seconds;
    
    resultCard.classList.remove('d-none');
    
    // Scroll to results
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorAlert.classList.remove('d-none');
    
    // Scroll to error
    errorAlert.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function copyResult() {
    const paraphrasedText = document.getElementById('paraphrasedText').textContent;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(paraphrasedText).then(() => {
            showToast('Result copied to clipboard!');
        }).catch(() => {
            fallbackCopyText(paraphrasedText);
        });
    } else {
        fallbackCopyText(paraphrasedText);
    }
}

function fallbackCopyText(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('Result copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy text:', err);
        showToast('Failed to copy text. Please copy manually.');
    }
    
    document.body.removeChild(textArea);
}

function showToast(message) {
    // Create a simple toast notification
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 end-0 p-3';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="toast show" role="alert">
            <div class="toast-body bg-success text-white">
                ${message}
            </div>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        document.body.removeChild(toast);
    }, 3000);
}

// Example texts for quick testing
const exampleTexts = [
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
    "Climate change refers to long-term changes in global temperatures and weather patterns, primarily caused by human activities such as burning fossil fuels.",
    "The internet has revolutionized the way we communicate, work, and access information, connecting people from all corners of the world.",
    "Renewable energy sources like solar and wind power are becoming increasingly important as we work to reduce our dependence on fossil fuels."
];

// Add example text functionality (you could add buttons for this)
function useExampleText(index = 0) {
    if (index < exampleTexts.length) {
        document.getElementById('inputText').value = exampleTexts[index];
        document.getElementById('inputText').dispatchEvent(new Event('input'));
    }
}
