# LookingGlass

**Konomi Systems** - Distributed AI compute without GPUs.

## Overview

LookingGlass maps enterprise architecture to a cube-based compute mesh.
Systems stabilize at the Frumkin equilibrium: κ = φ⁻¹ ≈ 0.618.

## Components

| Module | Description |
|--------|-------------|
| eVGPU | Pure CPU tensor operations |
| FemtoLLM | 16-dim nano language model |
| BlockArray | Sparse 1000³ compute grid |
| Cube | 9-node unit (8 vertices + center) |

## Quick Start

```python
from src.core import KonomiSystem

ks = KonomiSystem()
ba = ks.create_block_array("main", (10, 10, 10))
cube = ks.create_cube("c1")
cube.connect("NEU", "SWD")
```

## Standards

Layers 0-9: Meta, Base UDTs, ISA-95, ISA-88,
ISA-101, ISA-18.2, OPC-UA, Sparkplug, Modbus, KPIs.

## Architecture

Enterprise hierarchy (L0-L4) maps directly to
cube topology. See `docs/` for the full site.

## Tests

```bash
pip install -e . && pytest
```
