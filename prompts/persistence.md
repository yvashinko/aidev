Role: backend engineer.
Context: [spec, existing ORM models].
Task: add persistence for [ENTITY]: ORM model, migration, repository interface.
Requirements:
- Migration must be reversible.
- Repository returns domain types, not ORM.
- No generic `Repository<T>`.
Quality: destructive ops require explicit comment; migration tested locally.
