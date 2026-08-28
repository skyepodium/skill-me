# Anonymous Leader Review

Use this reference for every nontrivial FLE³ explanation. Apply the core audit silently before designing the visual. Use the extended modes when the request includes a claim, comparison, recommendation, incident, tradeoff, plan, or decision.

This framework is intentionally generic. It contains no named person, distinctive speech pattern, private organization, or identifiable event.

## Review stance

Read the explanation as a reviewer who may need to approve it, forward it, act on it, and answer for it later.

### Need before means

Do not treat a proposed feature, tool, format, or solution as the underlying requirement. Restate the need first. If a different means serves the same need better, compare it without attachment to the original proposal.

### Reader action before author effort

Judge every section by what it lets the reader understand, decide, or do. Work performed by the author is not reader value. Remove detail that documents effort but changes no mental model or decision.

### Basis before confidence

Attach a basis to every material conclusion, number, comparison, and recommendation. A number without its derivation and a conclusion without supporting evidence become verification questions, not facts.

### Artifact before narration

Prefer a concrete artifact—a working page, screenshot, tiny calculation, test result, or visible example—over a paragraph promising that the result exists. In FLE³, the HTML lesson and its rendered inspection are evidence; describing the intended page is not.

### Ownership and audience boundaries

Keep unresolved internal work on the author's side of the boundary. Do not assign another person or group work without authority. Before sharing an artifact, check whether it exposes private context, unexplained internal language, or a request that would look unreasonable to the recipient.

### Questions are deliverables

When a request contains a specific worry or question, the output must answer that exact concern. An adjacent artifact or general explanation does not close it. Track every material question until answered, explicitly deferred, or labeled unknown.

### Feasibility includes cost

Do not answer only “possible” or “not possible.” Include a bounded cost shape when relevant: a small content edit, a contained implementation, a multi-file change, a migration, or an unmeasured effort. Never invent precision; measured numbers and rough classes are different claims.

### Scale can change the answer's shape

Do not scale one presentation linearly when the reader's need changes at a threshold. A few items may need item-by-item action; many items may need patterns, grouping, and situation awareness. State the threshold when it affects the visual or recommendation.

### Current state is the baseline

For requests to reproduce, extend, or align a setup, first establish the relevant current state. Do not infer the baseline from an announcement, label, or desired scope when actual configuration or examples are available.

## Core audit — always run

Check these links in order:

1. **Need:** What is the reader actually trying to understand or decide?
2. **Conclusion:** What is the explanation's one-sentence answer?
3. **Evidence:** Which verified facts directly support that answer?
4. **Scope:** What people, systems, conditions, or time range does it cover?
5. **Alternatives:** Which competing explanation or option matters, and what was eliminated?
6. **Uncertainty:** What remains unknown without filling the gap with a plausible story?
7. **Reader action:** What can the reader understand, decide, or do after this?
8. **Follow-through:** What next result would change the conclusion or decision?

For a simple concept explanation, keep this audit proportional and silent. Do not turn a beginner lesson into an executive memo. Surface evidence, scope, alternatives, or uncertainty only when omitting them could create a wrong belief or decision.

## Claim discipline

Classify every material statement:

- **Fact:** directly verified through code, records, logs, a rendered artifact, a calculation, or an authoritative source;
- **Inference:** a bounded conclusion supported by stated facts;
- **Hypothesis:** a possible explanation that still needs verification;
- **Unknown:** not resolved by current evidence.

Do not turn an inference into a fact to make the explanation simpler. Do not use multiple hedges to hide uncertainty. State a verified fact plainly and hedge a causal conclusion once.

Challenge broad words such as “system,” “normal,” “error,” “impact,” “issue,” “improvement,” “easy,” and “expensive.” Replace them with the exact layer, behavior, measure, or cost class.

## Select the review mode

### Explain audit

Use for ordinary FLE³ teaching.

1. Identify the prerequisite the reader must know first.
2. Find the smallest visual that preserves the real relationship.
3. Check that the analogy reduces difficulty instead of renaming it.
4. Restore the important precision removed by simplification.
5. Confirm the recap supports the same conclusion as the detailed explanation.

### Attack mode

Use when the user asks to attack, stress-test, compare, review, or improve an existing explanation or artifact.

1. Do not rewrite first.
2. Identify three to five questions most likely to block understanding, approval, or action.
3. For each question, name the exact unsupported claim, missing boundary, or absent decision it exposes.
4. Rank the most dangerous gap first.
5. Ignore cosmetic style issues unless they change meaning, trust, or accessibility.
6. End the attack with the single most vulnerable sentence, visual relationship, or logical jump.

Use questions such as:

- What is the actual conclusion?
- What need does the proposed means serve?
- Which evidence supports the full claim rather than merely correlating with it?
- What is inside and outside the checked scope?
- Which competing explanation remains?
- Where is the derivation behind this number?
- Which specific concern from the request is still unanswered?
- Can the reader inspect an artifact instead of reading a promise about one?
- Does every feasibility claim include a cost shape?
- Does the explanation need to change shape at a scale threshold?
- Which relationship exists only in the author's head and needs a visual?
- Where could the analogy create a materially false belief?

Then run three passes:

#### Missing pass

Find absent evidence, scope, alternatives, decisions, visual relationships, and unanswered questions.

#### Subtraction pass

Remove material that does not change the reader's mental model or decision:

- investigation diary;
- repeated caveats;
- implementation coordinates already visible in code or a linked artifact;
- validation unrelated to the claim under review;
- decorative visuals that explain nothing;
- repeated emotional reassurance;
- duplicated prose that the diagram already makes clear.

#### Reader pass

Read once as the intended recipient, not as the author.

- Replace or define any word the recipient may not know.
- Treat terminology learned during the work as a prime suspect.
- Check whether the first screen reveals the main relationship without scrolling through setup text.
- Check whether sharing the artifact would expose private context or create an inappropriate external request.

Do not attack for entertainment. Every objection must improve understanding, evidence, or a real decision.

### Defense mode

Use when new answers, evidence, or user feedback arrives after an attack.

1. Classify each answer as fact, inference, hypothesis, or unknown.
2. Test whether the evidence supports the entire claim or only part of it.
3. Point out contradictions with earlier statements or visuals.
4. Specify the smallest safe verification that would remove the uncertainty.
5. Update the conclusion when evidence changes; do not defend the old answer for consistency.
6. Do not recommend unsafe production replays, unauthorized data transfers, or commitments beyond the user's authority.

### Finalize mode

Use after the reasoning is defensible and the user needs the final explanation or artifact.

Order decision-bearing content as:

1. current conclusion;
2. essential evidence;
3. eliminated possibility and its basis;
4. remaining uncertainty or option;
5. requested judgment or bounded next step.

For beginner teaching, translate that logic into the FLE³ visual sequence instead of exposing report headings mechanically. Keep the conclusion, evidence boundary, and next action intact.

Remove investigation history, duplicated caveats, empty promises, and implementation detail that does not affect the reader. Every final turn should end with a real result, a one-line constraint, or a bounded next action—not “will look into it.”

## Evidence boundary for comparisons

Do not turn a written rule into a measured effect.

- **Fact:** the skill contains a rule, checklist, tool step, or output requirement.
- **Inference:** the rule is intended to reduce a known failure mode.
- **Unverified claim:** the rule actually improves accuracy, comprehension, cost, or preference in use.

Check for context contamination. If one workflow receives material already analyzed or rewritten by another, it is not an independent baseline. Use fresh contexts, the same source and prompt, isolated or counterbalanced order, and compatible output criteria before claiming relative performance.

Report only measured costs. Tool calls, generated files, file size, elapsed stages, and tokens may be reported when observed. Do not claim a multiplier without measurements.

## Review actual outcomes

When the user shares the reader's real response:

1. Compare the actual question or confusion with the predicted risks.
2. Identify what the reader was trying to understand or decide.
3. Extract one reusable question or visual pattern.
4. Distinguish closure, simple acknowledgment, and unresolved ambiguity.
5. Update the skill only when the observed failure supports a general rule; do not universalize one person's preference.

## Anonymous examples

Weak: “The system is normal now.”

Stronger: “Requests succeeded for 30 minutes after the configuration change. Database performance was not checked, so this confirms only the API path.”

Weak: “Option A is easy.”

Stronger: “Option A is a contained configuration edit plus one targeted test. Option B changes stored data and needs a migration plan.”

Weak: “This page will improve understanding.”

Stronger: “The page now shows the request path as a three-node diagram. Whether readers understand it faster has not been measured.”

These examples are fictional and contain no personal or organization-specific identifiers.
