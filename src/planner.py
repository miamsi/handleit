import os
import json
from groq import Groq

class SchemaPlanner:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
    def propose_schema(self, profile: dict) -> str:
        """Uses Groq to suggest a clean data engineering schema based on the profile."""
        system_prompt = (
            "You are an expert Data Engineer. Analyze the provided Excel workbook profile. "
            "Propose a normalized database schema. "
            "Return a structured plan detailing: 1. Tables to create, 2. Columns per table, 3. Suggested data types. "
            "Do not write code, only return the structural design."
        )
        
        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the workbook profile:\n{json.dumps(profile, indent=2)}"}
            ],
            model=self.model,
            temperature=0.2
        )
        return completion.choices[0].message.content
