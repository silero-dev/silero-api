"""The same client drives every hosted model listed in silero_api.MODELS."""
from silero_api import Client, MODELS

client = Client()
for slug, info in MODELS.items():
    print(slug, "->", info["category"], "required:", info["required"])
# pick one explicitly
output = client.run({"text": "The quiet part of the morning is the only hour that still belongs to you."}, model="elevenlabs/tts")
print(output)
