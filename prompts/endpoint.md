Role: senior backend engineer.
Context: [SERVICE spec, AGENTS.md, existing models].
Task: add a new REST endpoint: [METHOD] [PATH].
Requirements:
- Input DTO with validation.
- Output DTO.
- Error mapping per ProblemDetails.
- Service contract.
- Unit + integration tests.
Quality: do not expose ORM entities; idempotent where applicable.
