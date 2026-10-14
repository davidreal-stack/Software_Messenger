# Domain Overview

MISSION-002 implements four infrastructure-independent, immutable domain entities in `app/domain`:

- **Contact:** UUID identity, nonblank trimmed name, and a normalized telephone string checked against the minimal syntax rule in DECISION-003.
- **Message:** UUID identity and nonblank logical content. It has no recipient, provider, encoding, or transport-length state.
- **MessageAttempt:** UUID identity, message ID, recipient contact ID, pending/sent/failed status, optional generic provider reference, optional failure reason, and UTC creation/completion timestamps. A pending attempt may transition once to a terminal outcome.
- **Job:** UUID identity, pending/running/completed/failed status, and UTC lifecycle timestamps. It is only a domain record; it does not execute or schedule work.

Entities use UUID4 defaults and standard-library types only. Values are frozen; transition methods return updated values. The recipient maximum of five remains an application/business operation rule and is not enforced by these individual entities because no send operation or service is in scope here.

The phone rule checks syntax only; it does not establish that a number exists, is assigned, or is reachable. See `docs/ai-workflow/DECISIONS.md` for the decisions made where the prior conceptual documents left details open.
