import os
import requests
import json
from typing import List, Dict, Any

class DeepSeekService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

    def _call_api(self, messages: List[Dict[str, str]], model: str = "deepseek-chat") -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling DeepSeek API: {str(e)}")
            raise

    def summarize_video(self, transcript: str, language: str = "zh-CN") -> Dict[str, Any]:
        """
        Summarize video transcript using DeepSeek API.
        Returns structured JSON data.
        """
        
        system_prompt = f"""
        You are an expert video content summarizer. Your task is to analyze the provided video transcript and generate a structured summary in {language}.
        
        The output must be a valid JSON object with the following structure:
        {{
            "full_summary": "A comprehensive summary of the video content (approx. 20% of original length)",
            "key_points": [
                {{
                    "title": "Key Point Title",
                    "content": "Detailed explanation of the key point"
                }}
            ],
            "chapters": [
                {{
                    "title": "Chapter Title",
                    "summary": "Summary of this specific section",
                    "timestamp": "HH:MM:SS (if available in text, else null)"
                }}
            ],
            "terminology": {{
                "term1": "Definition/Explanation",
                "term2": "Definition/Explanation"
            }}
        }}
        
        Ensure the summary captures:
        1. Core arguments and conclusions
        2. Key data and statistics
        3. Important examples
        
        Do not include any markdown formatting (like ```json) in the response, just the raw JSON string.
        """
        
        user_prompt = f"Here is the video transcript:\n\n{transcript[:20000]}..." # Truncate if too long, handling chunking in future
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_text = self._call_api(messages)
        
        # Clean up potential markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback for parsing error
            return {
                "full_summary": response_text,
                "key_points": [],
                "chapters": [],
                "terminology": {}
            }
