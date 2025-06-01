# Input Layer - Multimodal Interface

```mermaid
flowchart TD
  subgraph Input
    A1[Text Input (Web UI/API)]
    A2[Voice Input (Whisper)]
    A3[Image Input (CLIP)]
  end

  subgraph DirectorAgent
    D1[Director Agent]
  end

  subgraph Processing
    W1((Whisper))
    C1((CLIP))
  end

  A1 --> D1
  A2 --> W1 --> D1
  A3 --> C1 --> D1
```
