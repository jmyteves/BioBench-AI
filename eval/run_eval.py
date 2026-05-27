"""
BioBench AI — automated evaluation runner
Runs all 30 prompts against any OpenAI-compatible API endpoint and saves results.

Usage:
    python run_eval.py --model gpt-4o --api-key YOUR_KEY
    python run_eval.py --model claude-opus-4-5 --provider anthropic --api-key YOUR_KEY
    python run_eval.py --model gemini-1.5-pro --provider google --api-key YOUR_KEY

Output:
    results/<model_name>_<timestamp>.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

PROMPTS_PATH = Path(__file__).parent.parent / "prompts" / "prompts.json"
RESULTS_DIR  = Path(__file__).parent.parent / "results"

PROVIDERS = {
    "openai":    {"base_url": "https://api.openai.com/v1",           "key_env": "OPENAI_API_KEY"},
    "anthropic": {"base_url": "https://api.anthropic.com/v1",        "key_env": "ANTHROPIC_API_KEY"},
    "google":    {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai", "key_env": "GOOGLE_API_KEY"},
    "xai":       {"base_url": "https://api.x.ai/v1",                 "key_env": "XAI_API_KEY"},
}

SYSTEM_PROMPT = (
    "You are an expert molecular biologist and cell biologist with deep knowledge of "
    "epigenomics, stem cell biology, and experimental design. Answer the following question "
    "with the depth and precision expected in a high-quality scientific discussion. "
    "Do not hedge unnecessarily. Reason mechanistically."
)


def load_prompts():
    with open(PROMPTS_PATH) as f:
        data = json.load(f)
    return data["prompts"]


def query_model(prompt_text: str, model: str, base_url: str, api_key: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("Install openai package: pip install openai")

    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt_text},
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content


def empty_scores():
    return {"novelty": 0, "tractability": 0, "mechanistic_depth": 0, "confounder_awareness": 0}


def run_eval(model: str, provider: str, api_key: str, dry_run: bool = False):
    prompts   = load_prompts()
    base_url  = PROVIDERS[provider]["base_url"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path  = RESULTS_DIR / f"{model.replace('/', '-')}_{timestamp}.json"
    RESULTS_DIR.mkdir(exist_ok=True)

    results = {
        "benchmark":   "BioBench AI",
        "version":     "1.0.0",
        "model":       model,
        "provider":    provider,
        "timestamp":   timestamp,
        "system_prompt": SYSTEM_PROMPT,
        "prompts":     [],
    }

    print(f"\nBioBench AI  |  model: {model}  |  {len(prompts)} prompts\n{'-'*60}")

    for i, p in enumerate(prompts, 1):
        print(f"[{i:02d}/30] category={p['category']}  id={p['id']}", end="  ", flush=True)

        if dry_run:
            response = "[DRY RUN — no API call made]"
        else:
            try:
                response = query_model(p["prompt"], model, base_url, api_key)
                time.sleep(0.5)         # rate-limit buffer
            except Exception as e:
                response = f"ERROR: {e}"
                print(f"FAILED — {e}")

        results["prompts"].append({
            "id":            p["id"],
            "category":      p["category"],
            "prompt":        p["prompt"],
            "response":      response,
            "scores":        empty_scores(),    # fill in manually or extend script
            "total":         0,
            "notes":         "",
        })
        print("done" if not dry_run else "skipped (dry-run)")

    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved → {out_path}")
    print("Next: open results file, add scores (1-4) per dimension, then re-run analysis.")
    return out_path


def analyse(results_path: str):
    """Print a quick summary of a scored results file."""
    with open(results_path) as f:
        data = json.load(f)

    dim_keys = ["novelty", "tractability", "mechanistic_depth", "confounder_awareness"]
    dim_totals = {k: 0 for k in dim_keys}
    scored = 0

    for p in data["prompts"]:
        t = sum(p["scores"].values())
        if t > 0:
            scored += 1
            for k in dim_keys:
                dim_totals[k] += p["scores"].get(k, 0)

    if scored == 0:
        print("No scored prompts found. Add scores (1–4) to each dimension in the results file.")
        return

    print(f"\nBioBench AI Summary  —  {data['model']}")
    print(f"Scored: {scored}/30 prompts\n")
    print(f"{'Dimension':<25} {'Total':>8} {'Avg /4':>8} {'Max':>6}")
    print("-" * 50)
    for k in dim_keys:
        avg = dim_totals[k] / scored
        print(f"{k.replace('_',' ').title():<25} {dim_totals[k]:>8} {avg:>8.2f} {scored*4:>6}")

    overall_avg = sum(dim_totals.values()) / (scored * len(dim_keys))
    print(f"\nOverall average score: {overall_avg:.2f} / 4.00")


def main():
    parser = argparse.ArgumentParser(description="BioBench AI runner")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run evaluation against a model")
    run_p.add_argument("--model",    required=True, help="Model name (e.g. gpt-4o, claude-opus-4-5)")
    run_p.add_argument("--provider", default="openai", choices=PROVIDERS.keys())
    run_p.add_argument("--api-key",  default=None,  help="API key (or set env var)")
    run_p.add_argument("--dry-run",  action="store_true", help="Skip API calls, save empty responses")

    ana_p = sub.add_parser("analyse", help="Summarise a scored results file")
    ana_p.add_argument("results_file", help="Path to a results JSON file")

    args = parser.parse_args()

    if args.command == "run":
        provider_conf = PROVIDERS[args.provider]
        api_key = args.api_key or os.environ.get(provider_conf["key_env"])
        if not api_key and not args.dry_run:
            sys.exit(f"Provide --api-key or set {provider_conf['key_env']} env var")
        run_eval(args.model, args.provider, api_key or "dry-run", args.dry_run)

    elif args.command == "analyse":
        analyse(args.results_file)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
