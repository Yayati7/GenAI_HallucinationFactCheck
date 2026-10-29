# GenAI Hallucination Fact Check

A small Python program that compares responses to an original prompt and a refined prompt using a locally running Ollama model.

## Requirements

- Python 3
- [Ollama](https://ollama.com/download)
- A pulled model, for example `ollama pull llama3.2`

Start Ollama, then run from this folder:

```powershell
python main.py
```

To run one prompt only, use `python main.py --prompt original` or `python main.py --prompt refined`. To choose another model, use `python main.py --model MODEL_NAME`.
