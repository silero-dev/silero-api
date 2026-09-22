# Silero API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/xiaomi/mimo-tts?utm_source=github&utm_medium=ugc&utm_campaign=silero-dev&utm_content=readme-badge&utm_term=tier-a)

Silero Models is a set of compact, CPU-friendly speech models from Silero: text-to-speech, speech-to-text, voice activity detection and text enhancement, loaded through `torch.hub` with a few lines of code. This package is a Python client that gives you a Silero API for the two jobs most people reach for, speaking text and transcribing audio, with `pip install silero-api` and without installing PyTorch at all.

You get a blocking `run()` that returns the finished audio or transcript, a submit-and-poll path for long files, webhook delivery for servers that must not block, and a single runtime dependency (`requests`). It is meant for backend services, batch jobs and notebooks that need speech in and speech out as a function call.

> **Try it now:** [https://synexa.ai/explore/xiaomi/mimo-tts](https://synexa.ai/explore/xiaomi/mimo-tts?utm_source=github&utm_medium=ugc&utm_campaign=silero-dev&utm_content=readme-top&utm_term=tier-a) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Silero](#about-silero)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **No PyTorch in your deployment.** Silero is light, but it still pulls in `torch` and `torchaudio`, which adds hundreds of megabytes to a container image and a CUDA decision to every deploy. This client depends on `requests` only.
- **Wider language coverage.** Silero's public STT checkpoints cover English, German, Spanish and Ukrainian, and its TTS a handful of languages. The hosted `openai/whisper-v3` endpoint transcribes 99 languages, and `elevenlabs/tts` reads 29 to 74 depending on model.
- **Voice cloning and expressive delivery.** Silero TTS offers fixed speaker IDs. `xiaomi/mimo-tts` clones a voice from a 10 to 30 second clip, invents one from a text description, and follows style tags such as `(sigh)`.
- **Per-run pricing with no server to run.** `xiaomi/mimo-tts` is $0.02 per run, `elevenlabs/tts` $0.05 and `openai/whisper-v3` $0.004. Nothing sits idle between calls.

## Installation

```bash
pip install git+https://github.com/silero-dev/silero-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=silero-dev&utm_content=readme-apikey&utm_term=tier-a)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import silero_api

output = silero_api.run({
    "text": "Hello, this is a test of MiMo speech synthesis."
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from silero_api import Client

client = Client(api_key="sk-...")
output = client.run({"text": "Hello, this is a test of MiMo speech synthesis."})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`xiaomi/mimo-tts`](https://synexa.ai/explore/xiaomi/mimo-tts?utm_source=github&utm_medium=ugc&utm_campaign=silero-dev&utm_content=readme-models&utm_term=tier-a) | text-to-audio | Xiaomi MiMo V2.5 text-to-speech. Speaks text with one of 9 built-in voices, clones a voice from a reference clip, or invents a new voice from a written description. | $0.02 |
| [`elevenlabs/tts`](https://synexa.ai/explore/elevenlabs/tts?utm_source=github&utm_medium=ugc&utm_campaign=silero-dev&utm_content=readme-models&utm_term=tier-a) | text-to-audio | ElevenLabs text to speech. Reads text aloud in one of 21 built-in voices, across 29 languages on the default model and up to 74 on Eleven v3. | $0.05 |
| [`openai/whisper-v3`](https://synexa.ai/explore/openai/whisper-v3?utm_source=github&utm_medium=ugc&utm_campaign=silero-dev&utm_content=readme-models&utm_term=tier-a) | speech-to-text | Whisper large v3 transcribes or translates speech from an audio file, in 99 languages. | $0.004 |

The default model is **`xiaomi/mimo-tts`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `xiaomi/mimo-tts`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | yes | `Hello, this is a test of MiMo speech syn…` | — | Text to speak. A style tag may lead the text, e.g. '(happy)Hello there'; inline tags such as '(sigh)' are also supported. Tags are never spoken out loud. |
| `voice` | string | no | `Dean` | mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean | Built-in voice. Mutually exclusive with reference and description |
| `reference` | file | no | — | — | A .wav/.mp3 clip whose voice gets cloned (Optional). 10-30 seconds of clean speech works best. Mutually exclusive with voice and description |
| `description` | string | no | — | — | A sentence that invents a new voice, e.g. 'man in his forties, deep and raspy, speaks slowly' (Optional). Every call invents a slightly different voice. Mutually exclusive with voice and reference |
| `instructions` | string | no | — | — | Plain-language style note, e.g. 'slow down, sound tired' (Optional). Never spoken out loud. Not allowed together with description, which already carries the style |
| `audio_format` | string | no | `wav` | wav, mp3 | Output audio format |

### `elevenlabs/tts`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | yes | `The quiet part of the morning is the onl…` | — | The text to speak. Billed per character; the pool's free accounts hold 10,000 characters each |
| `voice` | string | no | `Adam` | Adam, Alice, Bella, Bill, Brian, Callum, Charlie, Chris, … | One of the 21 built-in ElevenLabs voices. All are English speakers, but they read other languages accurately with a multilingual model, in an English accent |
| `model_id` | string | no | `eleven_multilingual_v2` | eleven_multilingual_v2, eleven_v3, eleven_v3_conversation… | Synthesis model. multilingual_v2 is the most stable for long text (29 languages), v3 is the most expressive and understands [audio tags] (74 languages, 5,000 characters), flash/turbo are the fastest |
| `output_format` | string | no | `mp3_44100_128` | mp3_44100_128, mp3_44100_96, mp3_44100_64, mp3_44100_32, … | Audio container, as codec_samplerate_bitrate. Higher-fidelity formats (mp3_44100_192, pcm_44100, wav_44100) need a paid ElevenLabs tier and are not available here |
| `stability` | number | no | `0.5` | 0, 1 | How steady the delivery is. Lower is more emotional and more variable between generations, higher is more monotone |
| `similarity_boost` | number | no | `0.75` | 0, 1 | How closely the output sticks to the original voice |
| `style` | number | no | `0` | 0, 1 | Style exaggeration. Anything above 0 costs extra latency |
| `use_speaker_boost` | boolean | no | `True` | — | Boost similarity to the original speaker, at a small latency cost |
| `speed` | number | no | `1.0` | 0.7, 1.2 | Speaking rate. 1.0 is normal; the API accepts 0.7 to 1.2 and refuses anything outside it |
| `language_code` | string | no | — | — | ISO 639-1 code forcing a language for synthesis and text normalization, e.g. 'ja'. Ignored by eleven_multilingual_v2, which detects the language itself |
| `apply_text_normalization` | string | no | `auto` | auto, on, off | Whether numbers, dates and abbreviations are spelled out before being spoken. 'auto' lets the model decide |
| `seed` | integer | no | — | 0, 4294967295 | Best-effort deterministic sampling: the same seed, text and settings return the same audio. Determinism is not guaranteed |

### `openai/whisper-v3`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `audio_url` | file | yes | — | — | Audio to transcribe (.mp3/.mp4/.m4a/.wav/.webm/.ogg) |
| `task` | string | no | `transcribe` | transcribe, translate | Task to perform on the audio file. Either transcribe or translate. |
| `language` | string | no | `en` | af, am, ar, as, az, ba, be, bg, bn, bo, br, bs, ca, cs, c… | Language of the audio file. If translate is selected as the task, the audio will be translated to English, regardless of the language selected. If `None` is passed, the language will be automatically detected. This will also increase the inference time. |
| `chunk_level` | string | no | `segment` | — | Level of the chunks to return. |
| `max_segment_len` | integer | no | `29` | 10, 29 | Maximum speech segment duration in seconds before splitting. |
| `merge_chunks` | boolean | no | `True` | — | Whether to merge consecutive chunks. When enabled, chunks are merged if their combined duration does not exceed max_segment_len. |
| `version` | string | no | `3` | — | Version of the model to use. All of the models are the Whisper large variant. |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from silero_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Silero

Silero Models is an open collection of production-oriented speech models maintained by Silero and published in the `snakers4/silero-models` repository. The family covers speech-to-text (English, German, Spanish and Ukrainian checkpoints), text-to-speech (the v3 and v4 models, with Russian, English, German, Spanish, French, Ukrainian, Uzbek, Kalmyk, Tatar and several Indic languages), text enhancement for restoring punctuation and capitalisation, and the separately released Silero VAD, which is widely used as a lightweight voice activity detector in streaming pipelines.

The design goal is the opposite of most research models: small checkpoints, single-pass inference, no external dependencies beyond PyTorch, and real-time or faster performance on a single CPU thread. The TTS models expose a fixed set of named speakers per language, accept SSML for pauses, emphasis and rate, and render at 8, 24 or 48 kHz. The STT models are enterprise-grade for their size but were not trained for the broad accent and noise coverage that large transformer transcribers now offer.

The practical limits follow from that scope. Voices are natural but clearly synthetic compared with current neural TTS, there is no voice cloning or emotional direction, transcription quality degrades on far-field or heavily accented audio, and language coverage is narrow. For many embedded and on-device uses those trade-offs are exactly right; for a content or product pipeline they are usually the reason to look elsewhere.

The hosted endpoints used by this client are different models that provide the same capabilities: `xiaomi/mimo-tts` and `elevenlabs/tts` for text-to-speech and `openai/whisper-v3` for speech-to-text; the original Silero weights are available at https://github.com/snakers4/silero-models if you want to self-host. Voice activity detection is not covered by this client; Silero VAD remains the right tool for that and runs comfortably on CPU.

**Official project:** https://github.com/snakers4/silero-models

## Use cases

- **Read notifications aloud** — call `run()` with the message as `text` and a built-in `voice` to get an audio file for IVR or accessibility features.
- **Transcribe call recordings** — pass an `audio_url` to the `openai/whisper-v3` endpoint with `task="transcribe"` and receive timestamped segments.
- **Translate foreign-language audio** — set `task="translate"` on the same endpoint to get an English transcript regardless of the source language.
- **Clone a narrator** — give `xiaomi/mimo-tts` a 10 to 30 second `reference` clip and it speaks new text in that voice.
- **Multilingual voiceovers** — use `elevenlabs/tts` with `model_id="eleven_multilingual_v2"` and a `language_code` for stable long-form narration in 29 languages.
- **Subtitle generation at scale** — submit a folder of videos without blocking, then assemble captions from the `chunk_level` segments delivered to your webhook.

## FAQ

**Is there a Silero API?**

Silero publishes its models as open checkpoints loaded through `torch.hub`, not as a hosted REST API. This package wraps Synexa endpoints that provide the same text-to-speech and speech-to-text capabilities over HTTPS, so you do not need PyTorch or a model download.

**How much does the Silero API cost?**

Text-to-speech through `xiaomi/mimo-tts` is $0.02 per run and through `elevenlabs/tts` $0.05 per run. Speech-to-text through `openai/whisper-v3` is $0.004 per run. Billing is per completed run.

**Can I run Silero without a GPU?**

Yes, Silero itself is designed for CPU. The reason to use this client is not the GPU but the dependency footprint, the language coverage and the voice quality: the hosted endpoints give you Whisper-class transcription in 99 languages and cloneable, expressive voices without shipping PyTorch.

**Does this client work with the original snakers4/silero-models repo or Silero VAD?**

No. It does not load Silero checkpoints, expose Silero speaker IDs, or run voice activity detection. It is an HTTP client for the hosted endpoints only. For VAD, use Silero VAD directly; it is small and runs on CPU.

**What input formats does it accept?**

For text-to-speech only `text` is required; `xiaomi/mimo-tts` optionally takes one of `voice`, `reference` (.wav or .mp3) or `description`, plus `instructions` and `audio_format`. For speech-to-text `audio_url` is required and accepts .mp3, .mp4, .m4a, .wav, .webm or .ogg, with optional `task`, `language`, `chunk_level` and `max_segment_len`.

**Is this the official Silero SDK?**

No. This is an independent client and is not affiliated with Silero. The official project is at https://github.com/snakers4/silero-models.

## Related

- [Silero Models (official repository)](https://github.com/snakers4/silero-models)
- [Synexa Python client](https://github.com/synexa-ai/synexa-python)
- [xiaomi/mimo-tts on Synexa](https://synexa.ai/explore/xiaomi/mimo-tts)
- [elevenlabs/tts on Synexa](https://synexa.ai/explore/elevenlabs/tts)
- [openai/whisper-v3 on Synexa](https://synexa.ai/explore/openai/whisper-v3)

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Silero. Model weights and trademarks belong to their respective owners.

_Last reviewed: 2026-09-22_
