# src/services/ai_service.py
import torch
from utils.custom_logging import logger
from configs.model_config import MAX_INPUT_LENGTH, MAX_OUTPUT_LENGTH, AI_TEMPERATURE

class AIService:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def generate_response(self, user_message):
        """Generate a response from the AI model based on the user's message."""
        try:
            # Prepare the context for the model
            context = f"User: {user_message}\nAI:"
            
            # Tokenize the input
            inputs = self.tokenizer(context, return_tensors="pt", padding=True, truncation=True, max_length=MAX_INPUT_LENGTH)
            inputs = inputs.to(self.model.device)  # Move inputs to the same device as the model
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=MAX_OUTPUT_LENGTH,
                    num_return_sequences=1,
                    temperature=AI_TEMPERATURE
                )
            
            # Decode the response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.split("AI:")[-1].strip()  # Extract the AI's response
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request."