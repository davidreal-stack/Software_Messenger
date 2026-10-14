# Domain Model

```mermaid
classDiagram
    class Contact {
        UUID id
        string name
        string phone
    }
    class Message {
        UUID id
        string content
    }
    class MessageAttempt {
        UUID id
        UUID message_id
        UUID recipient_contact_id
        MessageAttemptStatus status
        string provider_reference
        string error
        datetime created_at
        datetime completed_at
    }
    class Job {
        UUID id
        JobStatus status
        datetime created_at
        datetime started_at
        datetime completed_at
        string error
    }
    Message "1" --> "0..*" MessageAttempt : logical message attempts
    Contact "1" --> "0..*" MessageAttempt : recipient by identifier
```

MISSION-002 implements these minimal domain fields. Optional values may be absent. MessageAttemptStatus is pending/sent/failed; JobStatus is pending/running/completed/failed. The attempt references message and recipient by UUID, not by persistence or provider models. `Job` intentionally has no execution engine or work relationship yet.
