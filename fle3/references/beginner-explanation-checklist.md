# Beginner Explanation Checklist

Use this checklist to review one FLE³ output, whether an HTML visual lesson or a narrow chat-only answer. It evaluates whether the output follows the intended beginner-friendly behavior. It does not establish parity with, or superiority over, a separate skill or plugin.

## Required behaviors

| Behavior | Review question | FLE³ requirement |
| --- | --- | --- |
| Zero assumed background | Can the reader start without domain knowledge? | Define every necessary domain term before use |
| Immediate orientation | Does the reader get the gist immediately? | Put a one-line answer first |
| Concrete mental model | Is there one familiar way to imagine it? | Use one analogy and map its parts explicitly |
| Visual support | Can the relationship be understood before reading all the prose? | In visual lesson mode, create a large HTML/SVG diagram; in chat-only mode, draw a compact inline diagram |
| Low cognitive load | Are too many new pieces introduced together? | Use at most three mechanism chunks at once |
| Accuracy recovery | Does the answer restore what simplification removed? | Include “비유와 다른 점” when material |
| Claim integrity | Are facts, inferences, hypotheses, and unknowns kept distinct? | Do not present a rule, analogy, or plausible story as measured fact |
| Understanding check | Can the reader verify the mental model? | Restate differently or ask one ten-second check |
| Speech fit | Does the wording match the user's register and requested simplicity? | Start directly, keep sentences short, and avoid counseling, baby talk, or fake praise |
| Decision usefulness | Can the reader act when a choice is required? | Add evidence, scope, uncertainty, and next action only when relevant |

## Failure conditions

Revise the answer when any of these is true:

- the first paragraph contains unexplained jargon;
- the reader must already know the category being explained;
- the analogy introduces more unfamiliar ideas than the original concept;
- visual lesson mode produces no HTML file or only a chat diagram;
- a process with multiple parts is described without a diagram;
- the main picture contains unexplained abbreviations or more than seven ungrouped nodes;
- the visual is decorative and does not explain a relationship;
- gradients, shadows, cards, animation, or decorative shapes remain without a teaching purpose;
- emoji, themed characters, or playful labels distract from the mechanism;
- the HTML was not visually rendered but the response claims visual QA;
- more than three new steps are presented before a recap;
- the analogy is presented as if it were literally the mechanism;
- an inference, hypothesis, or unmeasured effect is presented as a verified fact;
- the answer is accurate but still sounds like documentation or an executive memo;
- the answer is friendly but omits a limit that would cause a wrong conclusion;
- the answer repeats the reader's self-label, corrects it, or turns a level request into emotional counseling;
- the speech register does not match the user's language;
- reassurance delays the answer or a sentence carries multiple new ideas.

## Forward-test prompts

Use at least one process, one abstract concept, and one decision prompt when testing a new version.

- **Process:** “쿠버네티스가 컨테이너를 어떻게 관리하는지 처음 듣는 사람에게 설명해줘.”
- **Abstract concept:** “API가 뭔지 컴퓨터를 잘 모르는 사람도 이해하게 설명해줘.”
- **Decision:** “작은 동아리 명단을 종이로 관리할지 앱으로 관리할지 쉽게 비교해줘.”

Score gist, vocabulary, visual, analogy, mechanism, boundary, claim integrity, cognitive load, recap/check, and speech fit from 0 to 2. A result below 18/20 needs revision. Any zero in vocabulary, visual, mechanism, claim integrity, or speech fit is an automatic failure in visual lesson mode.

This score describes the reviewed output only. Do not report that the skill itself “scores 20/20” unless outputs were actually generated and independently scored under a recorded protocol.

## Controlled comparison protocol

Use this protocol before comparing FLE³ with another workflow:

1. Start each workflow in a fresh context with no prior explanation of the target.
2. Give both workflows the same source material and task prompt.
3. Run both orders across cases: A then B, and B then A, or use isolated sessions.
4. Preserve each workflow's intended output medium; do not score a chat answer as if it were an HTML artifact, or vice versa.
5. Score explanation quality separately from presentation quality, factual accuracy, output-medium fit, and user preference.
6. Record observable cost measures such as tool calls, stages, elapsed time, output files, bytes, and tokens when token counts are available.
7. Blind the reviewer to the producing workflow when practical.

Without this protocol, report only structural differences found in the skill files and observed steps from the specific run. Do not generalize them into performance claims.
