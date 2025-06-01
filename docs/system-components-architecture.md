# System Components Architecture

```mermaid
flowchart TD
  subgraph External Inputs
    Input1[Text (API, Web UI)]
    Input2[Voice (Whisper)]
    Input3[Image (CLIP)]
  end

  subgraph App Core
    DIR[Director Agent]
    PM[Project Manager Agent]
    DSG[Designer Agent]
    DEV[Dev-Implementor Agent]
    REV[Dev-Reviewer Agent]
    OPS[DevOps Agent]
  end

  subgraph Infra
    REDIS[(Redis - Pub/Sub)]
    POSTGRES[(Postgres - State)]
    GITHUB[(GitHub - Artifacts)]
    LOG[(Log - TBD)]
  end

  Input1 --> DIR
  Input2 --> Whisper --> DIR
  Input3 --> CLIP --> DIR

  DIR --> PM
  PM --> DSG
  PM --> DEV
  PM --> OPS
  DEV --> REV
  DEV --> GITHUB
  DSG --> PM
  REV --> PM
  OPS --> PM

  App Core --> REDIS
  App Core --> POSTGRES
  App Core --> LOG
```
