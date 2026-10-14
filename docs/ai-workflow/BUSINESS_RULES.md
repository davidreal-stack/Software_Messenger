# Business Rules

The following are confirmed requirements from the project mission. Rules describing eventual MVP behavior are requirements for future implementation, not evidence that the behavior exists today.

- **BR-001 — Recipient limit:** An operation may include at most five recipients in the initial MVP. Enforce the limit at the application/business layer. Reject an over-limit submission explicitly; never silently truncate it.
- **BR-002 — Telephone validity:** Each recipient must have valid telephone information before sending.
- **BR-003 — Confirmation:** Sending requires the user's explicit confirmation after reviewing the intended operation.
- **BR-004 — Per-recipient outcome:** Each recipient attempt must eventually have a recorded success or failure result.
- **BR-005 — No silent discard:** If the recipient maximum is exceeded, report rejection explicitly and do not silently discard recipients.

## Future ideas

Support for approximately 1,000–10,000 contacts is a future scalability direction, not permission to implement bulk messaging in the current phase. The roadmap is planning context only.
