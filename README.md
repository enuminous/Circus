# CIRCUS — Circularity and Information-leakage Audit

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/Circus) · This repository is linked through its source; GitHub Pages is not enabled.
<!-- ENUMINOUS-NETWORK:END -->

**Zoo animal specification · version 1.0.0**

CIRCUS audits how support for a claim was constructed. It traces each claim through operational definitions, data selection, labels, scoring, and validation; then identifies whether the claim, a conclusion derived from it, a fitted choice, or an expected result fed into evidence used to confirm it.

CIRCUS answers: **Could the claimed result have helped build the evidence that appears to support it?** It does not test general robustness to hostile nuisance changes; that is MONSTER’s job.

## Fixed operation

| Field | Definition |
|---|---|
| Purpose | Detect circular support, information leakage, post-selection, and dependent validation. |
| Inputs | Frozen claim(s), operational definitions, provenance records, data/label/scoring/validation lineage, and decision thresholds. |
| Transformation | Build a directed provenance/dependency graph; mark claim-derived or outcome-informed choices; assess each path from claim to confirming evidence. |
| Outputs | Provenance map; named circularity/leakage risks; independent-check plan; gate decision; evidence-status table. |
| Pass | Every material claim-to-evidence path is broken by frozen methods and independently sourced labels/checks; no material unresolved path remains. |
| Fail | A material feedback path remains, or a purported independent check inherits the same claim-conditioned choices. |
| N/A | Provenance for a material field/path is missing or cannot be established. N/A is never a pass. |

## Required procedure

1. **Freeze the target.** Record exact claim text, version/date, scope, operational definitions, predicted direction, thresholds, exclusions, and intended population. Ambiguity is logged, not silently repaired.
2. **Inventory the evidence pipeline.** For every claim, trace operational definition → data source/selection → labels/annotation → scoring/metrics → validation/split → reported result. Add preprocessing, exclusions, tuning, stopping rules, and publication selection where relevant.
3. **Draw dependencies.** Use directed edges `informs`, `selects`, `defines`, `labels`, `tunes`, `scores`, `validates`, or `reports`. Record the concrete artifact, actor/tool, and timestamp for each node and edge.
4. **Mark feedback.** Flag paths where the claim, expected answer, observed outcome, fitted parameter, or success-selected example affected evidence construction or the choice of a confirming analysis.
5. **Judge materiality.** A path is material if breaking it could plausibly change the result, the sample, the label, the score, the uncertainty, or the decision. State the reason.
6. **Require independent checks.** Specify how each material path is severed: frozen protocol and code, held-out data not used for design/tuning, independently sourced labels, blinded adjudication, or independent replication. “Different split” alone does not establish independence when choices were shared.
7. **Classify.** Apply the gate rules below and preserve unresolved risks and negative findings.

## Gate rules

- **PASS** only if all material provenance is documented and every material feedback path is broken using frozen methods and independently sourced labels/checks. The result must also be reproducible from the recorded artifacts.
- **FAIL** if any material feedback path remains, if an “independent” check depends on claim-informed labels or tuning, or if post-selection can explain the confirmation.
- **N/A** for a specific field/path whose provenance is missing. The overall audit cannot PASS while a material path is N/A. If nonmaterial provenance is N/A, explain why it cannot affect the result.
- Never convert missing evidence into evidence of independence. Never infer a pass from a low risk count.

## Risk taxonomy

| Risk ID | Name | Trigger |
|---|---|---|
| C-01 | Definition echo | Operational definition encodes the target conclusion or expected signature. |
| C-02 | Selection on success | Included cases, windows, examples, or exclusions were chosen because they showed the desired result. |
| C-03 | Label contamination | Labels were generated, adjudicated, or corrected using the claim, output, or expected answer. |
| C-04 | Score/tuning feedback | Metric, threshold, weights, or model settings were selected after inspecting confirmatory outcomes. |
| C-05 | Split leakage | Training/tuning and validation share subjects, events, time windows, derived artifacts, or information channels. |
| C-06 | Validation inheritance | A purportedly independent check inherits claim-conditioned definitions, labels, preprocessing, or thresholds. |
| C-07 | Selective reporting | Only successful endpoints, seeds, cohorts, or analyses are reported. |
| C-08 | Provenance gap | A material lineage record is missing; mark N/A, not pass. |

## Repository contents

- `animal.yaml`: concise operation card and gate logic.
- `schemas/report.schema.json`: machine-readable report contract.
- `templates/audit-report.json`: fill-in report.
- `examples/demo-report.json`: illustrative *not passed* audit with a missing provenance path.
- `src/circus.py`: standard-library report gate checker.
- `tests/`: gate behavior tests.

## Validate a report

Requires Python 3.10+; no third-party packages.

```sh
python -m unittest discover -s tests -v
python src/circus.py templates/audit-report.json
python src/circus.py examples/demo-report.json
```

The checker verifies the decision gate, not scientific truth or completeness of submitted provenance. Independent human review and artifact-level verification remain necessary. `FAIL` and `N/A` are distinct: failure means a known gate is unmet; N/A means required lineage cannot be established.

## Report minimum

For each claim, record a stable ID, exact statement, operational definition, evidence pipeline nodes and edges, circularity risks, path materiality, independent check, status, and artifact/source reference. See the JSON schema and template.

## Scope boundary

CIRCUS focuses on **evidence ancestry and support construction**. It does not claim that a non-circular result is robust, causally valid, novel, or true. Use MONSTER for robustness under preregistered nuisance shifts; use other Zoo animals for their specified proof, dimensional, novelty, or empirical operations.

## License

CC0-1.0. See `LICENSE`.
