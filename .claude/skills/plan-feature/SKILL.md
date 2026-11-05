---
name: plan-feature
description: Interview the user, read the relevant code, and write a plan to docs/plans/<feature>.md, then stop for approval. Use when the user wants to plan a new feature or bigger change.
argument-hint: [feature-name]
disable-model-invocation: true
---
Plan the feature: $ARGUMENTS
1. Ask up to 3 simple questions about edge cases (skip if clear).
2. Read only the code that matters.
3. Write the plan to `docs/plans/$ARGUMENTS.md`: goal, steps, how each step is checked.
4. Stop and wait for approval before changing any code.
