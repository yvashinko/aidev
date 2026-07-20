Role: senior engineer using a local LLM.
Context: [file diff, AGENTS.md].
Task: perform a code review.
Requirements:
- Minimum 5 comments with priority.
- Flag AI-typical issues (missing error handling, secrets, SQL injection).
- Mark false positives.
Quality: every comment references a specific line and includes a suggestion.
