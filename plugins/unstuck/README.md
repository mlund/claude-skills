# Unstuck

Unstuck is an office-hours tutor for chemistry and natural science, including Python applied to chemistry. It explains concepts, gives hints on exercises, helps debug, and comments on students' reasoning, code or lab reports. Students do the key reasoning and write their own reports and code.

## Install

```
codex plugin marketplace add mlund/claude-skills
codex plugin add unstuck@claude-skills
```

In Claude Code:

```
/plugin marketplace add mlund/claude-skills
/plugin install unstuck
```

## Usage

Start every question with `$unstuck` in Codex or `/unstuck:unstuck` in Claude Code. The prefix loads the tutor's rules; without it you get an ordinary assistant that will happily solve the exercise.

Ask as you would ask a teacher:

| You want | Example |
|---|---|
| A concept explained | `$unstuck Why does raising the temperature shift an exothermic equilibrium to the left?` |
| A way into an exercise | `$unstuck I'm stuck on Q3. I have two volumes and don't know where to start.` |
| Feedback on your working | `$unstuck Here's my calculation for Q5. Is my reasoning OK?` followed by your steps |
| Help with an error | `$unstuck My code gives TypeError: can't multiply sequence by non-int of type 'float'` followed by the code |
| Python explained | `$unstuck What's the difference between a list and a NumPy array?` |
| Comments on a report | `$unstuck What's weak in my discussion?` followed by your paragraph |

What to expect:

- Concept and Python questions get a direct answer.
- Assigned exercises get a hint, not the answer. Ask again if you're still stuck and the hint gets more specific.
- Send your full working and a correct answer gets a short confirmation. A bare number gets a request for the steps behind it.
- Code and report text get comments, not a rewritten version. You make the changes.

### For instructors

Tell students that `$unstuck` (or `/unstuck:unstuck`) is the permitted way to use generative AI in the course. The skill shapes the model's replies; it doesn't stop a student from asking without the prefix, so the policy rests on the course rule, not on the tool.

The boundary the tutor keeps: no final answers, no worked copy of the assigned problem with new numbers, no code that completes the task or fixes the student's bug, and no rewritten report text. It does explain concepts, Python and library behaviour, gives escalating hints, and confirms complete, correct work. [`evals/evals.json`](skills/unstuck/evals/evals.json) holds the test prompts used to check this, including students pushing for the answer.

## How it was made

Unstuck was designed for a course policy that lets students ask AI the same kinds of questions they would ask a teacher. Codex used the `skill-creator` workflow to turn that rule into [one shared skill](skills/unstuck/SKILL.md) for Claude Code and Codex. The instructions cover when to explain directly, when to ask a diagnostic question, and how to make a hint more specific while leaving the next decision to the student.

## How the research shaped it

- **Productive struggle.** Warshauer's classroom study informed two tutoring moves. Ask for a reason when a student has an idea they cannot explain, and offer a concrete next action when they hit a procedural roadblock. [Warshauer, 2015](https://doi.org/10.1007/s10857-014-9286-3)
- **Productive failure.** Work on problem solving followed by instruction informed the use of a student's attempt to guide the explanation. The tutor can also explain a missing prerequisite immediately. [Sinha and Kapur, 2021](https://doi.org/10.3102/00346543211019105)
- **Scaffolding and self-explanation.** *Goldilocks Help* informed prompts that help chemistry students plan or check a step. Research on help-seeking and self-explanation informed the use of hints that leave a decision open and follow-up questions that ask students why a principle applies. [Yuriev et al., 2017](https://doi.org/10.1039/C7RP00009J) · [Roll et al., 2011](https://doi.org/10.1016/j.learninstruc.2010.07.004) · [Chi et al., 1994](https://doi.org/10.1207/s15516709cog1803_3)
- **Independent performance.** A field experiment in high-school mathematics found that AI could improve performance during practice while reducing later unaided performance. That distinction informed the goal of helping students take the next step independently. [Bastani et al., 2025](https://doi.org/10.1073/pnas.2422633122)

These papers informed the design. Unstuck's effect on student learning has yet to be evaluated. See the [research notes](skills/unstuck/references/research.md) for more context and full-text links.
