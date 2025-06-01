# Agent Workflow Sequence (Build a Game to Teach AI Agents to Kids)

```mermaid
sequenceDiagram
  participant Human
  participant Director
  participant PM
  participant Designer
  participant DevImplementor
  participant DevReviewer
  participant DevOps
  participant GitHub

  Human->>Director: "Build a game to teach AI agents to kids"
  Director->>PM: Delegate task
  PM->>DevImplementor: Collaborate on requirements
  DevImplementor->>Designer: Provide implementation constraints
  PM->>Designer: Request wireframes and UX plan
  Designer-->>PM: Deliver wireframes and UX plan
  PM->>DevImplementor: Request implementation
  DevImplementor->>DevReviewer: Submit implementation
  DevReviewer-->>PM: Review feedback
  PM->>DevOps: Provision infra + monitoring
  DevOps-->>PM: Infra setup confirmation
  DevImplementor->>GitHub: Push source code
  PM->>Director: Aggregated status and results
  Director->>Human: Project update + summary
```
