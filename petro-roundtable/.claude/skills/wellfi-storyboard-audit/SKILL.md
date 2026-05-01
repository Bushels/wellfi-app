---
name: wellfi-storyboard-audit
description: Validate and prepare customer-facing WellFi storyboards, telemetry narratives, and Remotion video scenes against approved evidence before animation or rendering. Use when working on WellFi deployment storyboards, marketing videos, roundtable visual stories, scene planning, or claim-heavy animation for Obsidian or other WellFi runs, especially the April 2-3 run 3 evidence set for well 102161808317W509.
---

# WellFi Storyboard Audit

Use this skill before editing copy, timelines, scenes, or animations for a customer-facing WellFi run story.

## Default Evidence Set

Start from these files unless the user explicitly names a different well or run:

- `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\wellfi-run3-deployment-story.png`
- `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\run3-complete-timeline.md`
- `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\run3-narrative.md`
- `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\design-philosophy.md`
- `C:\Users\kyle\MPS\Obsidian\petro-roundtable\knowledge\wellfi-telemetry.md`
- Current Remotion source under `C:\Users\kyle\MPS\Obsidian\Data\Obsidian\Wells\102161808317W509\analysis\remotion-video\src\`

Treat the storyboard PNG plus the run 3 timeline as the approved visual brief unless raw logs or higher-confidence analysis contradict them.

## Workflow

1. Confirm the scope.
   - Identify the well, run number, customer, and exact date window.
   - Distinguish `approved storyboard`, `analysis narrative`, and `legacy animation`.
   - If the current Remotion composition tells a different story than the approved storyboard, stop and record the mismatch before editing.

2. Build a claim register.
   - For every proposed scene, overlay, headline, or callout, record:
     - claim text
     - status: `proven`, `inferred`, or `marketing framing`
     - source file
     - exact supporting value or event
     - validation owner
   - Do not animate a claim that has no source.

3. Use the roundtable agents in a lean order.
   - Use `production-data` to verify timestamps, event continuity, packet quality, pressure trends, and whether the displayed numbers match the approved run data.
   - Use `well-performance` to verify physical meaning. It decides whether wording like `pump startup`, `drawdown`, `fluid contact`, or `gas interference` is defensible.
   - Use `obsidian-energy` only for customer-facing framing and operator context after the engineering claims are locked.
   - Skip other engineering agents unless a specific scene needs them. More agents here usually adds noise, not quality.

4. Lock wording before motion.
   - Use `proven` only for direct measurements, logged events, or analysis statements that are explicitly confirmed.
   - Use `inferred`, `likely`, or `consistent with` when the story depends on interpretation.
   - Never present CRC-failed pressure or temperature values as real measurements.
   - Never let marketing language outrun the evidence. Make the visuals stronger, not the claims looser.

5. Decide what should pop.
   - Give each beat one dominant takeaway.
   - Reserve the biggest motion, contrast, or pause for evidence-backed moments such as:
     - first signal / peak signal
     - hit fluid
     - on bottom at the noise floor
     - pulled 1 joint
     - cable extension or signal improvement window
     - pump start and overnight drawdown
     - gas kick disruption and recovery
   - Avoid stacking multiple "hero" moments in one scene.

6. Preserve the design language.
   - Follow `Subterranean Signal` from `design-philosophy.md`.
   - Keep the canvas sparse, dark, and data-led.
   - Use restrained text and let the charts, path, and event markers carry the story.
   - Make events pop with timing, scale, glow, and contrast, not with extra clutter.

7. Run the pre-render checklist.
   - Check exact dates and times against the approved run window.
   - Check all unit conversions, especially BAR to kPa.
   - Check depth references for MD, TVD, and joint counts.
   - Compare the final pressure and temperature callouts against the run 3 docs.
   - Mark every unresolved conflict before rendering.
   - Render a proof and visually compare it against the approved storyboard PNG.

## Required Outputs

Produce these artifacts before final render approval:

- Source manifest: which files drive the animation
- Claim register: every scene tied to evidence
- Conflict list: any mismatched values, dates, or interpretations
- Beat map: which moments get the strongest visual emphasis
- Final validation note: why the animation is safe to show a customer

## Current Repo Warning

In this repository, the current Remotion files under `analysis\remotion-video\src\DeploymentStory*.tsx` and `analysis\remotion-video\src\data\deploymentData.ts` are legacy first-deployment material focused on a shorted transmission-path story. Do not assume they match the approved run 3 storyboard. Audit first, then replace or fork with the run 3 evidence set.
