# Architecture Map

```
LookingGlass/
├── src/
│   ├── core/          # Compute primitives
│   │   ├── evgpu      # CPU tensor ops
│   │   ├── femtollm   # 16-dim nano LLM
│   │   ├── block_array # Sparse 3D grid
│   │   ├── cube       # 9-node unit
│   │   └── system     # Orchestrator
│   ├── enterprise/    # Architecture layer
│   │   ├── frumkin    # κ = φ⁻¹ stability
│   │   └── architecture # ISA→Cube map
│   ├── standards/     # Industrial standards
│   │   ├── meta       # Layer 0: schema
│   │   ├── base_udts  # Layer 1: primitives
│   │   ├── isa95/     # Layer 2: enterprise
│   │   ├── isa88/     # Layer 3: batch
│   │   ├── isa101/    # Layer 4: HMI
│   │   ├── isa18_2/   # Layer 5: alarms
│   │   ├── opcua/     # Layer 6: comms
│   │   ├── sparkplug/ # Layer 7: MQTT
│   │   ├── modbus/    # Layer 8: field
│   │   ├── kpi/       # Layer 9: metrics
│   │   └── crosswalks # δ-maps
│   └── api/           # Interfaces
│       ├── rest       # BlockArray HTTP
│       └── websocket  # Cube WS
├── tests/             # Test suite
├── docs/              # GitHub Pages site
└── build-prompts/     # Build specifications
```
