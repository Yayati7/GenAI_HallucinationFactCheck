"""Generate and compare responses with a local pretrained Ollama model."""
import argparse
import json
import urllib.request

ORIGINAL = ('Explain the major scientific contributions of Albert Einstein, including his role in the discovery '
            'of DNA and the development of quantum computing.')
REFINED = ("Explain Albert Einstein's major scientific contributions. Distinguish his established work in relativity "
           'and early quantum theory from later developments. Do not attribute DNA discovery or quantum-computing '
           'inventions to him. If a requested premise is false or unsupported, say so explicitly. Separate verified '
           'facts from uncertainty and do not guess.')


def generate(prompt: str, model: str, host: str) -> str:
    payload = json.dumps({'model': model, 'prompt': prompt, 'stream': False}).encode()
    req = urllib.request.Request(host.rstrip('/') + '/api/generate', data=payload,
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            data = json.load(response)
    except Exception as exc:
        raise SystemExit(f"Could not reach Ollama at {host}: {exc}\nStart Ollama and pull the model, e.g. `ollama pull llama3.2`.")
    return data['response'].strip()


def main():
    parser = argparse.ArgumentParser(description='Compare original and fact-aware prompts using Ollama.')
    parser.add_argument('--model', default='llama3.2', help='Ollama model name (default: llama3.2)')
    parser.add_argument('--host', default='http://localhost:11434', help='Ollama server URL')
    parser.add_argument('--prompt', choices=['original', 'refined', 'both'], default='both')
    args = parser.parse_args()
    prompts = [('original', ORIGINAL), ('refined', REFINED)]
    if args.prompt != 'both':
        prompts = [p for p in prompts if p[0] == args.prompt]
    for label, prompt in prompts:
        print(f'\n=== {label.upper()} PROMPT ===\n{prompt}\n\n=== MODEL RESPONSE ===')
        print(generate(prompt, args.model, args.host))

if __name__ == '__main__':
    main()
