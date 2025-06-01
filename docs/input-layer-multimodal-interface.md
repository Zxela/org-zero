# Input Layer - Multimodal Interface

```mermaid
flowchart TD
  subgraph Input
    A1[Text Input - Web UI/API]
    A2[Voice Input]
    A3[Image Input]
  end

  subgraph Processing
    P1[Whisper]
    P2[CLIP]
  end

  subgraph DirectorAgent
    D1[Director Agent]
  end

  A1 --> D1
  A2 --> P1 --> D1
  A3 --> P2 --> D1
```
