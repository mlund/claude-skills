# Unstuck

Unstuck is an office-hours tutor for chemistry and natural science. It explains concepts, gives hints on exercises, and comments on students' reasoning or lab reports. Students do the key reasoning and write their own reports.

## How it was made

Unstuck was designed for a course policy that lets students ask AI the same kinds of questions they would ask a teacher. Codex used the `skill-creator` workflow to turn that rule into [one shared skill](skills/unstuck/SKILL.md) for Claude Code and Codex. The instructions cover when to explain directly, when to ask a diagnostic question, and how to make a hint more specific while leaving the next decision to the student.

## How the research shaped it

- **Productive struggle.** Warshauer's classroom study informed two tutoring moves. Ask for a reason when a student has an idea they cannot explain, and offer a concrete next action when they hit a procedural roadblock. [Warshauer, 2015](https://doi.org/10.1007/s10857-014-9286-3)
- **Productive failure.** Work on problem solving followed by instruction informed the use of a student's attempt to guide the explanation. The tutor can also explain a missing prerequisite immediately. [Sinha and Kapur, 2021](https://doi.org/10.3102/00346543211019105)
- **Scaffolding and self-explanation.** *Goldilocks Help* informed prompts that help chemistry students plan or check a step. Research on help-seeking and self-explanation informed the use of hints that leave a decision open and follow-up questions that ask students why a principle applies. [Yuriev et al., 2017](https://doi.org/10.1039/C7RP00009J) · [Roll et al., 2011](https://doi.org/10.1016/j.learninstruc.2010.07.004) · [Chi et al., 1994](https://doi.org/10.1207/s15516709cog1803_3)
- **Independent performance.** A field experiment in high-school mathematics found that AI could improve performance during practice while reducing later unaided performance. That distinction informed the goal of helping students take the next step independently. [Bastani et al., 2025](https://doi.org/10.1073/pnas.2422633122)

These papers informed the design. Unstuck's effect on student learning has yet to be evaluated. See the [research notes](skills/unstuck/references/research.md) for more context and full-text links.
