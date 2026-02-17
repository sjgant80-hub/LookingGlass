"""SharedFace — shared vertex node between two adjacent Cubes.

When two Cubes are adjacent, the vertices they share become one
FemtoLLM instance visible from both sides. This is the topological
collapse that makes data flow between cubes without duplication.

Before connect():
    cube_a.vertices['NEU']  ≠  cube_b.vertices['SEU']
    Two separate FemtoLLMs, no shared state.

After connect_cubes(cube_a, 'N', cube_b):
    cube_a.vertices['NEU']  IS  cube_b.vertices['SEU']
    cube_a.vertices['NWU']  IS  cube_b.vertices['SWU']
    cube_a.vertices['NED']  IS  cube_b.vertices['SED']
    cube_a.vertices['NWD']  IS  cube_b.vertices['SWD']
    Same FemtoLLM object. Data processed or read from either
    cube on those vertices is the same data.

This is topologically equivalent to a winding number collapse:
before sharing, a path from cube_a → cube_b and back forms a
loop that doesn't contract (winding ≠ 0). After sharing, the
boundary is gone — the loop contracts. Winding = 0. No paradox.

Origin: MacCubeFACE Step 2 pattern (AirTrek/Birdhouse project).
Adapted to LookingGlass vertex naming (NESW + U/D).
"""


# Face-to-vertex mapping using LookingGlass NESW+UD naming.
# Each face is defined by which 4 vertices sit on it.
FACE_VERTICES = {
    'N': ('NWD', 'NED', 'NWU', 'NEU'),  # North face (front)
    'S': ('SWD', 'SED', 'SWU', 'SEU'),  # South face (back)
    'W': ('SWD', 'NWD', 'SWU', 'NWU'),  # West face (left)
    'E': ('SED', 'NED', 'SEU', 'NEU'),  # East face (right)
    'D': ('SWD', 'SED', 'NWD', 'NED'),  # Down face (bottom)
    'U': ('SWU', 'SEU', 'NWU', 'NEU'),  # Up face (top)
}

# When cube_a faces cube_b in direction X, cube_b faces back in OPPOSITES[X]
OPPOSITES = {
    'N': 'S', 'S': 'N',
    'E': 'W', 'W': 'E',
    'U': 'D', 'D': 'U',
}


def connect_cubes(cube_a, face_a: str, cube_b) -> tuple:
    """
    Connect two adjacent Cubes by making their touching vertices shared.

    The 4 vertices on face_a of cube_a and the 4 vertices on the
    opposite face of cube_b become the SAME FemtoLLM instances.
    cube_a's instances are kept; cube_b's touching vertices are
    replaced with references to cube_a's.

    Args:
        cube_a: First Cube (its vertices are kept as the shared objects)
        face_a: Which face of cube_a is touching cube_b.
                'N' = cube_b is to the north (front) of cube_a
                'S' = south (back), 'E' = east (right), 'W' = west (left)
                'U' = up (above), 'D' = down (below)
        cube_b: Second Cube (its touching vertices are replaced)

    Returns:
        Tuple of 4 vertex names that are now shared.

    Example:
        # cube_b is to the north of cube_a
        shared = connect_cubes(cube_a, 'N', cube_b)
        assert cube_a.vertices['NEU'] is cube_b.vertices['SEU']
    """
    if face_a not in OPPOSITES:
        raise ValueError(
            f"face_a must be one of {list(OPPOSITES)}, got {face_a!r}"
        )

    face_b = OPPOSITES[face_a]
    verts_a = FACE_VERTICES[face_a]
    verts_b = FACE_VERTICES[face_b]

    # Make cube_b's touching vertices IS cube_a's touching vertices
    for va, vb in zip(verts_a, verts_b):
        shared_node = cube_a.vertices[va]
        cube_b.vertices[vb] = shared_node

    # Record the connection in both cubes' edge maps
    cube_a.edges[f"face_{face_a}"].append(cube_b.id)
    cube_b.edges[f"face_{face_b}"].append(cube_a.id)

    return verts_a
