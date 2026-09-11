---
name: tersify
description: Run the tersify agent on the working-tree diff, named paths, or a commit message.
argument-hint: "[paths | commit message]"
disable-model-invocation: true
---

Delegate to the `tersify:tersify` agent; do not edit yourself. It runs on a cheaper model.

Arguments: $ARGUMENTS

- None: the agent covers the working-tree diff. If a commit is pending, draft its message and pass it along.
- Paths: pass them for a whole-file pass.
- Other text: a commit message to trim.

Tell the agent the intent behind the change in a sentence or two. It cannot see this conversation, and needs the intent to keep the right why.

When it returns, read `git diff` before reporting. Revert edits that drop a reason, change meaning, or touch code. Report the revised commit message and the flags.
