# Running the evals

`evals.json` holds the prompts; `files/` the fixtures. `{IN}` and `{OUT}` in a prompt stand for a
run's `input/` and `outputs/` directories.

## Keep baselines blind

The skill's guidance also lives in the SI template (its `AGENTS.md` and README). A baseline that can
see a local checkout of the template, or of this repository, isn't a baseline. So:

- Start the orchestrating session in a neutral directory (e.g. an empty scratch folder), not inside
  the template or this repository; subagents inherit its working directory.
- Tell every run to work only in its own run directory, and baselines not to read local checkouts of
  the template or of this repository; the template is fetched from GitHub, as a user's would be.

## Layout

    <workspace>/iteration-N/eval-<id>-<name>/
      eval_metadata.json
      with_skill/run-1/{input/,outputs/,grading.json,timing.json}
      without_skill/run-1/{input/,outputs/,grading.json,timing.json}

This is the layout skill-creator's `aggregate_benchmark` and `generate_review.py` expect. Copy
fixtures into each run's `input/`, and record their hashes first so "unchanged" can be checked.
Delete `.venv/` and caches from outputs before launching the viewer.

## Run prompt

    Execute this task as a user would want it done.
    [with skill]  Skill: first read <skill>/SKILL.md and follow it.
    Task: "<prompt with {IN}/{OUT} filled in>"
    Work only inside <run dir>. [baseline: Do not read local checkouts of
    template-for-supporting-information or claude-skills.]
    Run non-interactively: you cannot ask the user. Write questions you would ask, with the default
    you used, to <run dir>/outputs/QUESTIONS.md. Return your final report as your reply; don't
    write a report file.

Subagents may not be allowed to write report files, so the orchestrator saves each returned report
to `outputs/REPORT.md` for the viewer. Questions go in a file because the viewer and the graders
need them.
