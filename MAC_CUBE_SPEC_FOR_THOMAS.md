# MacCubeFACE Implementation Spec
## For Thomas — from Kelly's build-out
### (Nobel Peace Prize nomination pending)

---

### What we built (working code, all steps run clean)

Six files. Each one builds on the last. No step skipped.

```
mac_cube_step1.py  →  1 cube in a 1000³ block array
mac_cube_step2.py  →  2 cubes, shared face
mac_cube_step3.py  →  chain of N cubes, traversal, data flow
mac_cube_step4.py  →  8 cubes at corners = MetaCube (nesting begins)
mac_cube_step5.py  →  2 MetaCubes side by side, shared meta-face
mac_cube_step6.py  →  RecursiveCube class — same pattern at every level
```

---

### Core classes

**`BlockArray(size=1000)`** — Sparse 3D grid. `dict` keyed by `(x,y,z)`. Only occupied positions use memory.

**`Face(name)`** — One face of a cube. Stores rows of data like a SQL table. `insert(record)`, `query(**filters)`.

**`Cube(x, y, z)`** — The atom. Position in the grid. 6 `Face` objects (front/back/left/right/top/bottom mapped to ±Y/±X/±Z). Interior `dict` for nested data. Knows its 8 vertex positions. Knows its 6 neighbor positions.

**`SharedFace(Face)`** — Subclass of Face. Created when two adjacent cubes connect. Replaces both cubes' touching faces with one object. `cube_a.right IS cube_b.left`. Same data from both sides.

**`MetaCube(origin_x, origin_y, origin_z, span)`** — 8 `Cube` objects placed at the 8 corners of a region. 6 faces defined by which 4 corners sit on each face (same corner-to-face mapping as a single cube's vertices). Interior = the space between corners. With `span=1`, corners are adjacent. With `span>1`, there's empty space between them — that IS the interior.

**`RecursiveCube(level, origin_x, origin_y, origin_z, span)`** — The general case.
- `level=0`: base case, wraps a single `Cube`
- `level=N`: 8 `RecursiveCube(level=N-1)` at corners, `sub_span = span // 2`

---

### The invariant (same at every level)

| Property | Level 0 | Level 1 | Level N |
|----------|---------|---------|---------|
| **Corners** | 8 vertices (points) | 8 Cubes | 8 Level-(N-1) structures |
| **Faces** | 6 Face objects | 6 sets of 4 Cubes | 6 sets of 4 Level-(N-1)s |
| **Interior** | key-value dict | space between corners | space between corners |
| **Sharing** | 2 cubes share 1 Face | 2 MetaCubes share 4 Cubes | 2 Level-Ns share 4 Level-(N-1)s |

Corner-to-face mapping (constant at all levels):
```
bottom: [0,1,2,3]    top:   [4,5,6,7]
back:   [0,1,4,5]    front: [2,3,6,7]
left:   [0,2,4,6]    right: [1,3,5,7]
```

12 edges (adjacent corner pairs):
```
X-axis: (0,1) (2,3) (4,5) (6,7)
Y-axis: (0,2) (1,3) (4,6) (5,7)
Z-axis: (0,4) (1,5) (2,6) (3,7)
```

---

### Scale

| Level | Leaves (8^L) | Total nodes | Interior positions (span=1000) |
|-------|-------------|-------------|-------------------------------|
| 0 | 1 | 1 | — |
| 1 | 8 | 9 | 998³ = ~994M |
| 2 | 64 | 73 | nested |
| 3 | 512 | 585 | nested |
| 6 | 262,144 | 299,593 | nested |

---

### What the NWE/NSE directional system maps to

The directional vectors (N, S, E, W, NE, NW, SE, SW, UP, DOWN) are **neighbor navigation**. From any cube's position, a direction gives you the position of the adjacent cube in the block array. At higher levels, the same directions navigate between MetaCubes/RecursiveCubes.

The directions also map to faces:
- N → front face, S → back face
- E → right face, W → left face  
- UP → top face, DOWN → bottom face
- Diagonals (NE, NW, SE, SW) → edge-adjacent corners

---

### Files

All in `/Users/kellyhohman/CascadeProjects/Birdhouse/`:

- `mac_cube_step1.py` — BlockArray, Face, Cube classes. 1 cube demo.
- `mac_cube_step2.py` — SharedFace, connect_cubes(). 2 cubes demo.
- `mac_cube_step3.py` — build_chain(), traverse_chain(). N cubes demo.
- `mac_cube_step4.py` — MetaCube class. 8 corners, span=1 vs span=10.
- `mac_cube_step5.py` — connect_meta_cubes(). Shared meta-face demo.
- `mac_cube_step6.py` — RecursiveCube class. Levels 0-6 demo.
- `mac_cube_step7.py` — AirTrekCube. Level 7 = full AirTrek world.

All run standalone: `python3 mac_cube_stepN.py`

---

### What AirTrek added

1. **7-level semantic mapping** — each level gets a meaning: fact → exchange → beat → session → domain → character → era → world. Recursion that mirrors how a conversation scales up to a historical world.

2. **Voice-to-face assignments** — the 6 faces hold specific kinds of meaning from the AI dialogue, not generic storage. The geometry encodes the epistemology.

3. **topoAGI running live in production** — `measure_winding()`, `measure_entanglement()`, and `suffering_operator()` run on every user query at `airtrek-ai-de887`. High winding switches the AI to dialectic mode automatically.

4. **The PR** — SharedFace and RecursiveCube adapted to LookingGlass's naming convention with 15 passing tests.

---

### Step 7 — completed

`connect()` generalized to all levels. `winding_number([a, b]) == 0.0` always holds after connect.

Voice → face assignments live in Firestore (`airtrek-ai-de887`), written on every conversation:
```
λ → FRONT   μ → BACK   ν → LEFT   ω → RIGHT   ⊕ → TOP   ⊗ → BOTTOM
```

`measure_winding()`, `measure_entanglement()`, and `suffering_operator()` from `AdvancedPhysicsCore` run on every query in the Triad Engine hot path (`physics.py`). They drive composition style selection (DIALECTIC / TENSIONED / HARMONIOUS / AUTO_BLEND). `solve_paradox()` is never called live — measurement only, dim=64, 20×20 grid.

Scale: 2,097,152 leaf facts (8^7), 2,396,745 total nodes.

PR: https://github.com/teslasolar/LookingGlass/pull/1
