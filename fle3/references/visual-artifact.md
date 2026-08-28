# Visual HTML Artifact

Read this reference whenever FLE³ uses visual lesson mode.

## Deliverable contract

Create one self-contained `.html` file that opens directly in a browser.

- Use semantic HTML, inline CSS, and inline SVG.
- Avoid build steps and external runtime dependencies.
- Include `<meta name="viewport">`, a meaningful `<title>`, `lang`, and accessible labels.
- Keep the page useful without JavaScript. Add small interactions only when they improve learning.
- Save under `artifacts/fle3/<topic-slug>.html` unless the user selected another path.
- Link the finished file in the final response.

## Visual direction

The page should feel like a clear illustrated lesson, not a design showcase, dashboard, or long article.

- Give roughly 60–70% of the first screen to the main visual.
- Use one strong composition with a clear reading path.
- Use a neutral background, one surface, and one primary accent. Add a semantic warning or success color only when it carries meaning.
- Use large type, useful spacing, thin borders, small corner radii, and clear contrast.
- Use consistent color and shape for the same concept across the page.
- Prefer one large SVG flow, map, or comparison over many boxes or cards.
- Keep visible body text concise. Put detail behind optional disclosure only when necessary.
- Do not use gradients, glass effects, decorative blobs, large shadows, ornamental illustrations, or entrance animation.
- Do not use emoji, themed characters, playful labels, or a grid of cards as a substitute for one explanatory composition.
- Use motion only when motion itself explains order or causality, and honor `prefers-reduced-motion`.
- Before keeping a visual element, ask: “If I remove this, does understanding get worse?” If not, remove it.
- Support both desktop and mobile without horizontal scrolling.

## Diagram semantics

Choose the diagram from the question, not from decoration:

- **Process:** left-to-right or top-to-bottom flow with verb-labeled arrows.
- **Hierarchy:** tree with the parent concept visually dominant.
- **Comparison:** two aligned lanes using the same evaluation axes.
- **Cause and effect:** visible trigger, change, and result.
- **State change:** before/after or a short timeline.
- **System interaction:** actors and exchanged objects, not unlabeled boxes.

Keep the main diagram to 3–7 nodes. If more are needed, group them into named stages. Every arrow must explain what moves or changes.

## Content layout

1. **Hero:** one-line answer and a short orientation sentence.
2. **Main visual:** the largest element on the page.
3. **Analogy:** one familiar model with explicit concept mapping.
4. **Real mechanism:** no more than three steps at once.
5. **Boundary:** one visible note explaining where the analogy breaks.
6. **Recap:** one sentence using different words.

Do not duplicate the same paragraph in multiple sections. Do not fill the page with boilerplate reassurance.

## Tone inside the artifact

- Lead directly with the answer. Do not place reassurance or a welcome paragraph before the hero statement.
- Treat a blunt request for a very low explanation level as a complexity setting, not an emotional problem to discuss.
- Match the user's speech register consistently across headings and body text.
- Keep headings conversational and concrete.
- Never describe or grade the reader by intelligence level.
- Avoid fake enthusiasm, excessive emoji, counseling language, classroom grading language, and “쉽죠?” endings.
- End with a memorable content sentence, not praise for understanding.

## Verification loop

1. Run `python3 scripts/validate_visual.py <generated-html>` from the skill directory.
2. Open or render the HTML with an available browser or screenshot tool.
3. Inspect the first screen at desktop width and a narrow mobile width.
4. Confirm that the main relationship is understandable from the visual alone.
5. Check for clipped text, overlapping nodes, tiny labels, horizontal scroll, low contrast, and empty-looking regions.
6. Confirm that all technical terms are defined before use and every visual label uses the same noun as the prose.
7. Revise and render again when a material issue appears.

If browser rendering is unavailable, perform structural validation and explicitly say the file was not visually rendered. Never claim visual QA without opening the result.

## Template use

Start from [../assets/visual-lesson-template.html](../assets/visual-lesson-template.html) when it fits. Replace every `FLE3_*` marker, delete unused sections, and redesign the central SVG for the topic. The template is a shell, not a finished answer; changing only the words is insufficient when the concept needs a different diagram.
