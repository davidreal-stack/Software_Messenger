# Codex Agent Contract

For every requested mission, follow this workflow:

1. Read `docs/ai-workflow/PROJECT_CONTEXT.md`.
2. Read `docs/ai-workflow/CURRENT_STATE.md`.
3. Read relevant architecture documentation.
4. Read applicable business and operational rules.
5. Read relevant decisions.
6. Inspect the existing repository before changing code or documentation.
7. Identify conflicts before implementation.
8. Plan the requested mission and its acceptance criteria.
9. Implement only within the explicitly authorized mission scope.
10. Run appropriate tests after implementation changes and report results.
11. Update relevant documentation.
12. Update `docs/diagrams/project_structure.md` if the structure changed.
13. Update `docs/ai-workflow/CURRENT_STATE.md`.
14. Update `docs/ai-workflow/CHANGELOG.md` when appropriate.
15. Report exactly what changed.
16. Report tests executed and their results.
17. Report documentation updated.
18. Report unresolved issues.

If a requirement conflicts with an approved architectural decision, stop and report the conflict instead of improvising. The roadmap is not permission to implement future functionality. Preserve existing work, do not silently remove or replace functionality, and do not send real SMS without explicit authorization in a future mission. Follow `docs/ai-workflow/OPERATIONAL_RULES.md` for the full operating rules.

## Backend Learning Glossary

When a mission introduces an intermediate or advanced Python construct, a relevant standard-library operation, or a backend framework feature, check `docs/glossary/` first. If it is not documented, add a brief Spanish explanation of the syntax, what it does, how the project uses it, and why it is used. Keep the glossary incremental and tied to code that exists. Avoid trivial concepts, long generic tutorials, and entries for technologies not yet used. This glossary is backend-only; do not put frontend, CSS, or UI material there.
