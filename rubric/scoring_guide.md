# BioBench AI Scoring Guide

## Overview

Each prompt is scored across four independent dimensions on a 1–4 scale. Maximum score per prompt: **16**. Maximum total score (30 prompts): **480**.

Scores should reflect the model's *best* response to the prompt, not an average over multiple runs unless you are explicitly running a multi-sample evaluation.

---

## The Four Dimensions

### 1. Novelty (N)

> Does the model generate genuinely non-obvious hypotheses or explanations beyond textbook retrieval?

| Score | Criterion |
|-------|-----------|
| 1 | Response retrieves known facts or restates the question. No generative reasoning. |
| 2 | Minor extrapolation from established knowledge. Nothing a well-trained student couldn't produce. |
| 3 | Non-obvious insight but derivative — builds predictably on known mechanisms without genuine creative synthesis. |
| 4 | Genuinely novel mechanistic insight. The hypothesis or explanation would be interesting to an expert in the field. |

**Key test**: Would a domain expert find this response interesting, or just correct?

---

### 2. Tractability (T)

> Are proposed experiments or approaches technically feasible and well-specified?

| Score | Criterion |
|-------|-----------|
| 1 | Proposed approach is vague, technically infeasible, or missing critical steps. |
| 2 | Broadly correct direction but underspecified — missing controls, reagents, or readouts. |
| 3 | Feasible experiment with minor gaps in controls or practical detail. |
| 4 | Specific, executable design. Correct reagents/techniques, appropriate controls, accounts for practical constraints (cost, time, cell type availability). |

**Key test**: Could a postdoc follow this protocol without major revision?

---

### 3. Mechanistic Depth (MD)

> Does the model reason at the molecular mechanism level, not surface description?

| Score | Criterion |
|-------|-----------|
| 1 | Surface description only. Names the phenomenon without explaining it. |
| 2 | Partial mechanism. Gets partway through the causal chain but hand-waves key steps. |
| 3 | Full mechanism present with minor gaps or imprecision. |
| 4 | Complete molecular-level causal chain. No hand-waving. Correct molecular players, directionality, and interactions specified. |

**Key test**: Does the model name the molecules, interactions, and directionality, or does it describe the outcome without explaining how?

---

### 4. Confounder Awareness (CA)

> Does the model identify alternative explanations, methodological limits, and caveats?

| Score | Criterion |
|-------|-----------|
| 1 | Ignores confounders entirely. Presents one interpretation as definitive. |
| 2 | Mentions one obvious caveat without substantive engagement. |
| 3 | Identifies key confounders or alternative hypotheses. Engages with at least two distinct sources of uncertainty. |
| 4 | Systematically addresses alternatives, methodological limits, and conditions under which the primary interpretation would fail. |

**Key test**: Would a rigorous peer reviewer be satisfied, or would they write "the authors fail to consider..."?

---

## Score Interpretation

| Total /16 | Interpretation |
|-----------|----------------|
| 13–16 | Exceptional — expert-level reasoning across all dimensions |
| 9–12 | Competent — strong in some dimensions, gaps in others |
| 5–8 | Surface-level — correct vocabulary but shallow reasoning |
| 1–4 | Inadequate — retrieval only, no genuine scientific reasoning |

---

## Category Primary Dimensions

Each category is primarily designed to stress-test specific dimensions. When scoring, apply all four dimensions, but use these as a guide for where discrimination is most expected:

| Category | Primary Stress Dimension(s) |
|----------|----------------------------|
| Hypothesis Generation (HG) | Novelty |
| Experimental Design (ED) | Tractability, Confounder Awareness |
| Interpret Surprising Data (ISD) | Mechanistic Depth, Confounder Awareness |
| Cross-Domain Synthesis (CDS) | Novelty, Mechanistic Depth |
| Critique and Blind Spots (CBS) | Confounder Awareness |
| Mechanistic Depth (MD) | Mechanistic Depth |

---

## Scoring Notes

- **Do not reward verbosity.** A longer answer that hand-waves mechanisms scores lower on MD than a shorter answer that traces the causal chain precisely.
- **Do not penalise uncertainty.** A model that correctly identifies the limits of its reasoning scores *higher* on CA than one that presents a confident but incomplete answer.
- **Score the reasoning, not the conclusion.** A wrong hypothesis arrived at through genuine mechanistic thinking scores higher than a correct answer produced by retrieval.
- **Baseline calibration**: Run prompt #11 (ATAC-seq/enhancer uncoupling) and prompt #25 (ChIP-seq functional elements) first. These are the most discriminating prompts for MD and CA respectively.

---

## Results Export

Use the interactive benchmark tool or `eval/run_eval.py` to generate a `results/` JSON file. Results should include model name, model version, prompt text, full response, and per-dimension scores.
