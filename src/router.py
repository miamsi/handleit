import os
from groq import Groq

class GroqRouter:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # 2026 Tier routing optimization
        self.fast_model = "llama-3.1-8b-instant"
        self.reasoning_model = "llama-3.3-70b-versatile"

    def route_intent(self, user_prompt: str) -> str:
        """Uses 8B model to classify user intent instantly."""
        system_prompt = "Classify intent into: 'RETRIEVAL', 'MANIPULATION', 'SCHEMA_PROPOSAL'. Return only the word."
        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=self.fast_model,
            temperature=0.0
        )
        return completion.choices[0].message.content.strip()
