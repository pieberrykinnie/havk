# NLU Patterns

IrrigaBot uses a **minimal regex-driven NLU** layer defined in `backend/nlu/intents.yml`.
At runtime the parser loads these patterns and returns the first matching intent.

## Supported Intents (prototype)

| Intent | Example Utterances |
|--------|-------------------|
| `join` | "join", "start", "register please" |
| `done` | "done", "stop", "complete" |
| `leave` | "quit", "exit" |

Add additional intents by editing the YAML; no code change required.

## Multilingual Support

Incoming messages are normalised using [`unidecode`](https://pypi.org/project/Unidecode/) to strip accents and transliterate non-Latin scripts (e.g. Devanagari) into ASCII before regex matching.  Adding new languages therefore only requires appending transliterated keywords to `intents.yml` – no code changes needed.