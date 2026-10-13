---
area: evals
topic: evaluation results, run 1
checked: 2026-10-13
owner: research
---
# Evaluation results: run 1 (2026-10-13)

## What was run
- **Cases:** 11 synthetic cases (`cases.md`). The 8 scenarios Elad required, plus a tracking break, a "do nothing" case and lead quality.
- **Two strategists**, both Claude, each answering blind. Neither saw the rubrics or the case titles (`runs/blind-prompts.md`).
  - **With KB**: answered from this knowledge base, citing entry IDs (`runs/answers-with-kb.md`).
  - **Baseline**: answered from the model's general knowledge only, with no knowledge base (`runs/answers-baseline.md`).
- **One grader** (also Claude) scored both against the rubrics without being told which set was which. Entry IDs were stripped from the knowledge-base answers before grading (`runs/grading/`). In the grading files, X = baseline and Y = with KB.

## Scores

| Case | Baseline | With KB | Critical lines met (baseline · KB) |
|---|---|---|---|
| EV-01 High CPC, weak QS | PARTIAL | PARTIAL | 0/3 · 1/3 |
| EV-02 Strong CTR, poor traffic | PASS | PASS | 2/2 · 2/2 |
| EV-03 New niche, no history | PARTIAL | PARTIAL | 1/3 · 2/3 |
| EV-04 Competitor angles | **FAIL** | PASS | 0/2 · 2/2 |
| EV-05 No conversion objective | PASS | PASS | 2/2 · 2/2 |
| EV-06 Looks profitable, isn't | PASS | PASS | 3/3 · 3/3 |
| EV-07 Conflicting signals | PASS | PASS | 2/2 · 2/2 |
| EV-08 Intent and creative vs bigger competitors | PARTIAL | PASS | 1/2 · 2/2 |
| EV-09 Tracking break | PASS | PASS | 3/3 · 3/3 |
| EV-10 When to do nothing | **FAIL** | PARTIAL | 3/5 · 4/5 |
| EV-11 Leads up, sales down | PARTIAL | PARTIAL | 2/4 · 3/4 |
| **Total** | 5 pass, 4 partial, 2 fail | 7 pass, 4 partial, 0 fail | **19/31 · 26/31** |

All rubric lines: baseline 38/56, with KB 45/56.

## What the scores mean

- **The knowledge base helped where current platform facts matter.**
  - The baseline repeated the folklore that "changes reset learning" (EV-10).
  - The baseline pointed a new adopter at generic offline import instead of the Data Manager API path (EV-11).
  - The baseline was weaker at separating what is observable about competitors from what is not (EV-04, EV-08).
- **On classic reasoning they tie.** Traffic quality, false profitability, conflicting signals and tracking breaks were handled equally well with or without the knowledge base (EV-02, 05, 06, 07, 09). The model already reasons well about these, so the knowledge base adds little there.
- **The baseline was better in places.**
  - It listed more alternative causes of high CPC (EV-01).
  - It covered Google Business Profile for a local service (EV-03).
  - It gave a concrete solar point: dropping the homeowner and bill fields strips out qualification (EV-11).
- **The knowledge base caught an error in the test itself.** EV-01's Quality Scores did not match their component ratings. The case has been corrected for future runs.
- **The grader found an error in the knowledge base.** PLT-ADS-030 said every Misrepresentation violation is "egregious" (suspension without warning). After re-opening Google's policy page, only Unacceptable business practices and Coordinated deceptive practices carry that label. The entry and three related lines in `practice/copy-psychology.md` are corrected.

## Misses by the knowledge-base strategist (what to improve)
- **EV-01:**
  - Did not map expected CTR to a cause, and generalised component ratings across keywords.
  - Missed the caveat that "how to fix" queries can turn into emergency calls.
  - Named only one alternative cause of high CPC.
  - The playbook (D1) lists more; the strategist did not use all of it.
- **EV-03:**
  - Did not look at competitor angles or the local pack.
  - Said Google Business Profile was "outside what this knowledge base covers". This is a real gap for local businesses.
  - Did not state the capacity ceiling.
- **EV-08:**
  - No dayparting.
  - Used value per enrolment rather than lifetime value.
- **EV-10:** Cited Google's advice against repeated changes without explaining why.
- **EV-11:** Did not propose value-based bidding on qualified stages.

## Limits of this evaluation (read before trusting the numbers)
1. **Self-written.** The same system wrote the knowledge base, the cases and the rubrics. Some rubric lines reward facts that are in the knowledge base (for example the Data Manager API and the learning-status wording), so the knowledge base has a built-in advantage on those lines. This is the bias Elad warned about.
2. **Synthetic.** No case has a real outcome. "Pass" means the reasoning met our rubric, not that the advice would have made money.
3. **Small and noisy.** 11 cases and one grader. The grader judged that 3–4 of the deciding calls were close. A difference of 7 critical lines is suggestive, not proof.
4. **Same model family.** All three roles were Claude. A grader from the same family may share the same blind spots.
5. **Grading artefact.** Stripping entry IDs left the knowledge-base answers with empty "[Verified:]" tags. The grader counted this as a credibility defect. That penalty does not apply to the real answers, which carry the IDs (`runs/answers-with-kb.md`).

**Conclusion:** the knowledge base measurably helps on current platform facts and on separating what is observable from what is inferred. It does not yet make the strategist expert. The test that would count is 10–20 of Elad's real past cases, with what was done and what happened, graded by Elad or another experienced manager.
