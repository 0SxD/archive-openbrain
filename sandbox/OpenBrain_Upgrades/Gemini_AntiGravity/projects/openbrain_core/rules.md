# OpenBrain Core Rules
1. All orchestration must operate independent of the UI or Database implementation (Agnostic).
2. Never prompt a sub-agent without utilizing the extreme loop grading verification.
3. Strict zero-trust paths: Do not mutate parent files directly, invoke local agent_sync files instead.
