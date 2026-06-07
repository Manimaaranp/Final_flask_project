from services.ai_service import (
    AIService
)

response = AIService.generate_text(
    "Explain Python in one sentence."
)

print(response)