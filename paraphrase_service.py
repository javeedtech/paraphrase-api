import logging
import os
from typing import Optional
import requests
import json
import random
from vocabulary import COMPREHENSIVE_SYNONYMS

logger = logging.getLogger(__name__)

class ParaphraseService:
    def __init__(self):
        self.model_name = "Hugging Face API"
        self.is_loaded = True  # Always ready for API calls
        
        # Built-in paraphrasing patterns as fallback
        self.fallback_patterns = [
            lambda text: f"In other words, {text.lower()}",
            lambda text: f"To put it differently, {text}",
            lambda text: f"Simply stated, {text}",
            lambda text: f"Another way to express this: {text}",
            lambda text: f"Rephrased: {text}",
        ]
    
    def _load_model(self):
        """Mock model loading - using API approach instead"""
        self.is_loaded = True
        logger.info("API-based paraphrasing service ready")
    
    def paraphrase(self, text: str, max_length: int = 100, temperature: float = 0.7) -> str:
        """
        Paraphrase the given text using Hugging Face API or fallback patterns
        
        Args:
            text: Text to paraphrase
            max_length: Maximum length of output
            temperature: Sampling temperature for generation
            
        Returns:
            Paraphrased text
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # First try Hugging Face Inference API
            hf_result = self._try_hugging_face_api(text, max_length, temperature)
            if hf_result:
                return hf_result
            
            # Fallback to built-in patterns with intelligent modifications
            return self._intelligent_fallback_paraphrase(text, temperature)
            
        except Exception as e:
            logger.error(f"Error during paraphrasing: {str(e)}")
            raise Exception(f"Paraphrasing failed: {str(e)}")
    
    def _try_hugging_face_api(self, text: str, max_length: int, temperature: float) -> Optional[str]:
        """Try to use Hugging Face Inference API"""
        try:
            # Check if HF_TOKEN is available in environment
            hf_token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGINGFACE_TOKEN')
            
            if not hf_token:
                logger.info("No Hugging Face token found, using fallback method")
                return None
            
            api_url = "https://api-inference.huggingface.co/models/t5-small"
            headers = {"Authorization": f"Bearer {hf_token}"}
            
            payload = {
                "inputs": f"paraphrase: {text}",
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "do_sample": True
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '').strip()
                    if generated_text and generated_text.lower() != text.lower():
                        return generated_text
            
            return None
            
        except Exception as e:
            logger.warning(f"Hugging Face API failed: {str(e)}")
            return None
    
    def _intelligent_fallback_paraphrase(self, text: str, temperature: float) -> str:
        """Create intelligent paraphrases using linguistic patterns"""
        # Clean the input text first
        original_text = text.strip()
        
        # Check if the text already has paraphrasing prefixes and remove them
        prefixes_to_remove = [
            "in other words,", "to express this differently:", "another way to state this is:",
            "rephrasing this concept:", "simply put:", "put simply,", "in essence,",
            "to clarify:", "here's a different perspective:", "viewed another way:",
            "consider this rephrasing:"
        ]
        
        clean_text = original_text.lower()
        for prefix in prefixes_to_remove:
            if clean_text.startswith(prefix):
                original_text = original_text[len(prefix):].strip()
                break
        
        # Apply intelligent transformations
        paraphrased = self._apply_linguistic_transformations(original_text, temperature)
        
        return paraphrased
    
    def _apply_linguistic_transformations(self, text: str, temperature: float) -> str:
        """Apply various linguistic transformations to create meaningful paraphrases"""
        sentences = text.split('. ')
        transformed_sentences = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            # Apply different transformation techniques
            transformed = self._transform_sentence(sentence.strip(), temperature)
            transformed_sentences.append(transformed)
        
        return '. '.join(transformed_sentences)
    
    def _transform_sentence(self, sentence: str, temperature: float) -> str:
        """Transform a single sentence using various techniques"""
        words = sentence.split()
        
        if len(words) < 3:
            return sentence
        
        # Apply transformations based on temperature
        transformations = []
        
        # Always apply synonym replacement
        transformed = self._replace_synonyms(sentence)
        transformations.append(transformed)
        
        # Higher temperature = more transformations
        if temperature > 0.5:
            # Sentence restructuring
            restructured = self._restructure_sentence(sentence)
            transformations.append(restructured)
        
        if temperature > 0.8:
            # Active/passive voice changes
            voice_changed = self._change_voice(sentence)
            transformations.append(voice_changed)
        
        # Choose the best transformation (avoid identical results)
        best_transformation = sentence
        for t in transformations:
            if t.lower() != sentence.lower() and len(t) > len(best_transformation) * 0.8:
                best_transformation = t
                break
        
        return best_transformation
    
    def _replace_synonyms(self, sentence: str) -> str:
        """Replace common words with synonyms"""
        # Use comprehensive universal vocabulary database
        synonyms = COMPREHENSIVE_SYNONYMS
        
        words = sentence.split()
        for i, word in enumerate(words):
            # Clean word (remove punctuation for matching)
            clean_word = word.lower().strip('.,!?;:()""''')
            
            if clean_word in synonyms and random.random() < 0.7:  # 70% chance to replace
                # Preserve original punctuation and capitalization
                punctuation = ''.join(c for c in word if c in '.,!?;:()""''')
                replacement = synonyms[clean_word]
                
                # Maintain capitalization pattern
                if word[0].isupper() and len(word) > 0:
                    replacement = replacement[0].upper() + replacement[1:] if len(replacement) > 1 else replacement.upper()
                
                words[i] = replacement + punctuation
        
        return ' '.join(words)
    
    def _restructure_sentence(self, sentence: str) -> str:
        """Restructure sentence patterns"""
        # Simple restructuring patterns
        if 'because' in sentence.lower():
            parts = sentence.lower().split('because')
            if len(parts) == 2:
                return f"Due to {parts[1].strip()}, {parts[0].strip()}"
        
        if 'although' in sentence.lower() or 'while' in sentence.lower():
            connector = 'although' if 'although' in sentence.lower() else 'while'
            parts = sentence.lower().split(connector)
            if len(parts) == 2:
                return f"Despite {parts[1].strip()}, {parts[0].strip()}"
        
        if sentence.lower().startswith('in the past'):
            return sentence.replace('In the past', 'Previously', 1).replace('in the past', 'previously', 1)
        
        return sentence
    
    def _change_voice(self, sentence: str) -> str:
        """Attempt simple active/passive voice changes"""
        # Simple patterns for voice transformation
        if ' has ' in sentence and ' transformed ' in sentence:
            return sentence.replace('has transformed', 'transformed')
        
        if ' use ' in sentence:
            return sentence.replace('use', 'employ')
        
        if ' created ' in sentence:
            return sentence.replace('created', 'brought about')
        
        return sentence
    
    def _add_variations(self, paraphrased: str, original: str) -> str:
        """Add subtle variations to the paraphrased text"""
        # Simple synonym replacements for common words
        replacements = {
            'quick': 'fast', 'fast': 'rapid', 'big': 'large', 'small': 'tiny',
            'good': 'excellent', 'bad': 'poor', 'nice': 'pleasant',
            'important': 'crucial', 'very': 'extremely', 'really': 'truly'
        }
        
        words = paraphrased.split()
        for i, word in enumerate(words):
            clean_word = word.lower().strip('.,!?;:')
            if clean_word in replacements and random.random() < 0.4:
                # Preserve original punctuation
                punctuation = ''.join(c for c in word if c in '.,!?;:')
                words[i] = replacements[clean_word] + punctuation
        
        return ' '.join(words)
    
    def _clean_output(self, paraphrased: str, original: str) -> str:
        """Clean and validate the paraphrased output"""
        # Remove any unwanted prefixes or suffixes
        paraphrased = paraphrased.strip()
        
        # If output is identical or too similar, try alternative approaches
        if paraphrased.lower() == original.lower() or len(paraphrased) < 5:
            # Return a modified version with simple transformations
            paraphrased = f"In other words: {original}"
        
        return paraphrased
    
    def get_model_status(self) -> dict:
        """Get current model status"""
        return {
            'loaded': self.is_loaded,
            'model_name': self.model_name,
            'device': 'api' if self.is_loaded else 'offline'
        }
    
    def reload_model(self):
        """Reload the model (useful for error recovery)"""
        self.is_loaded = True
        logger.info("Service reloaded and ready")
