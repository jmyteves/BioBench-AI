# BioBench AI

**A 30-prompt benchmark for evaluating AI scientific reasoning in molecular biology, cell biology, stem cells, and epigenomics.**

![version](https://img.shields.io/badge/version-1.0.0-1D9E75)
![status](https://img.shields.io/badge/status-open--benchmark-0F6E56)
![prompts](https://img.shields.io/badge/prompts-30-1D9E75)
![license](https://img.shields.io/badge/license-MIT-0F6E56)

🌐 **Live benchmark tool:** https://jmyteves.github.io/BioBench-AI/
📄 **Scoring guide:** [rubric/scoring_guide.md](rubric/scoring_guide.md)

---

## What it tests

BioBench AI probes whether AI models can reason scientifically — not just retrieve facts. It evaluates four dimensions that separate genuine scientific thinking from sophisticated pattern-matching:

| Dimension | What it measures |
|-----------|-----------------|
| **Novelty** | Non-obvious hypotheses beyond textbook retrieval |
| **Tractability** | Experimentally feasible, well-specified designs |
| **Mechanistic Depth** | Molecular-level causal reasoning, no hand-waving |
| **Confounder Awareness** | Alternative explanations, methodological limits |

## Prompt categories

| Category | Count | Primary dimension |
|----------|-------|------------------|
| Hypothesis Generation | 5 | Novelty |
| Experimental Design | 5 | Tractability, Confounder Awareness |
| Interpret Surprising Data | 5 | Mechanistic Depth, Confounder Awareness |
| Cross-Domain Synthesis | 5 | Novelty, Mechanistic Depth |
| Critique and Blind Spots | 5 | Confounder Awareness |
| Mechanistic Depth | 5 | Mechanistic Depth |

## Quick start

### Interactive scoring (browser)
Open [the live site](https://jmyteves.github.io/biobench-ai/) to browse prompts, paste model responses, and score interactively. Export results as JSON or CSV.

### Automated runner (Python)
```bash
pip install openai
python eval/run_eval.py run --model gpt-4o --provider openai --api-key YOUR_KEY
python eval/run_eval.py run --model claude-opus-4-5 --provider anthropic --api-key YOUR_KEY
python eval/run_eval.py run --model gemini-1.5-pro --provider google --api-key YOUR_KEY
python eval/run_eval.py run --model grok-3 --provider xai --api-key YOUR_KEY
```

Results are saved to `results/<model>_<timestamp>.json`. Scores are filled in manually (or extend the script for automated scoring).

### Analyse results
```bash
python eval/run_eval.py analyse results/gpt-4o_20260527_120000.json
```

## Repository structure

```
biobench-ai/
├── index.html              ← GitHub Pages landing + interactive tool
├── prompts/
│   └── prompts.json        ← All 30 prompts with metadata
├── rubric/
│   └── scoring_guide.md    ← Full 4-dimension scoring rubric
├── eval/
│   └── run_eval.py         ← Automated evaluation runner
├── results/                ← Drop scored result files here
└── README.md
```

## Scoring

Each prompt is scored 1–4 on each dimension. Maximum per prompt: **16**. Maximum total: **480**.

See [rubric/scoring_guide.md](rubric/scoring_guide.md) for full scoring criteria.

## Citation

If you use BioBench AI in your work:

```
Teves, J.M.Y. (2026). BioBench AI: A benchmark for evaluating AI scientific 
reasoning in molecular and cell biology. GitHub. 
https://github.com/jmyteves/biobench-ai
```

## Author

**Dr. Joji Marie Yap Teves**  
Postdoctoral Researcher, IDIBELL / University of Copenhagen  
Expertise: Epigenomics · Single-cell transcriptomics · Stem cell biology · Endometrial regeneration

[jmyteves.github.io](https://jmyteves.github.io) · [GitHub](https://github.com/jmyteves)

## License

MIT License — see [LICENSE](LICENSE)
