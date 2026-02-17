# Konomi System Build Spec

## Components
- eVGPU: CPU-based AI/ML (no GPU needed)
- FemtoLLM: 16-dim nano model, 4MB RAM
- BlockArray: 1000³ compute grid
- Cube: 8 vertices + 1 central node

## Performance Targets
- FemtoLLM: 0.1s/req, 4MB RAM
- eVGPU: 100% CPU util, 0 GPU
- BlockArray: Sparse storage for 1B cubes
- Cube: 9 concurrent LLMs
- Kontainer: <2GB total footprint

## Build Order
eVGPU → FemtoLLM → BlockArray →
Cube → APIs → Kontainer

## Optimize For
CPU efficiency, memory, network, cache
