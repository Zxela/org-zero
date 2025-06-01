# Input Layer - Multimodal Interface

```mermaid
flowchart TD
  subgraph Input
    A1[Text Input (Web UI/API)]
    A2[Voice Input (Whisper)]
    A3[Image Input (CLIP)]
  end

  subgraph DirectorAgent
    D1["Director Agent"]
  end

  A1 --> D1
  A2 --> Whisper((Whisper)) --> D1
  A3 --> CLIP((CLIP)) --> D1
```
