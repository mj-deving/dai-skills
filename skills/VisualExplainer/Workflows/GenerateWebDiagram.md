# GenerateWebDiagram Workflow

<!-- Voice DEACTIVATED
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the GenerateWebDiagram workflow in the VisualExplainer skill"}' \
  > /dev/null 2>&1 &
```
-->

**First action:** Read `${CLAUDE_SKILL_DIR}/MasterReference.md` to load the full visual-explainer skill context.

---

Load the visual-explainer skill, then generate an HTML diagram for: $@

Follow the visual-explainer skill workflow. Read the reference template and CSS patterns before generating. Pick a distinctive aesthetic that fits the content — vary fonts, palette, and layout style from previous diagrams.

If `surf` CLI is available (`which surf`), consider generating an AI illustration via `surf gemini --generate-image` when an image would genuinely enhance the page — a hero banner, conceptual illustration, or educational diagram that Mermaid can't express. Match the image style to the page's palette. Embed as base64 data URI. See CssPatterns.md "Generated Images" for container styles. Skip images when the topic is purely structural or data-driven.

Write to `${AGENT_HOME}/diagrams/` and open the result in the browser.
