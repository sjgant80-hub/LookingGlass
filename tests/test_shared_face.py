"""Tests for shared_face and RecursiveCube."""
from src.core.cube import Cube
from src.core.shared_face import connect_cubes, FACE_VERTICES, OPPOSITES
from src.core.recursive_cube import RecursiveCube, FACE_CORNERS


# ============================================================
# SharedFace tests
# ============================================================

def test_connect_cubes_shares_vertices():
    """After connect_cubes(), touching vertices are the same object."""
    a = Cube("a")
    b = Cube("b")
    connect_cubes(a, 'N', b)

    # North face of a: NWD, NED, NWU, NEU
    # South face of b: SWD, SED, SWU, SEU
    assert a.vertices['NWD'] is b.vertices['SWD']
    assert a.vertices['NED'] is b.vertices['SED']
    assert a.vertices['NWU'] is b.vertices['SWU']
    assert a.vertices['NEU'] is b.vertices['SEU']


def test_connect_cubes_non_touching_vertices_independent():
    """Non-touching vertices remain independent after connect."""
    a = Cube("a")
    b = Cube("b")
    connect_cubes(a, 'N', b)

    # South face of a should NOT be shared with anything
    assert a.vertices['SWD'] is not b.vertices['SWD']


def test_connect_cubes_records_edge():
    """connect_cubes records the connection in both cubes' edge maps."""
    a = Cube("a")
    b = Cube("b")
    connect_cubes(a, 'E', b)
    assert 'b' in a.edges['face_E']
    assert 'a' in b.edges['face_W']


def test_connect_cubes_all_directions():
    """connect_cubes works for all 6 directions."""
    for face in ('N', 'S', 'E', 'W', 'U', 'D'):
        a = Cube(f"a_{face}")
        b = Cube(f"b_{face}")
        shared = connect_cubes(a, face, b)
        assert len(shared) == 4

        opposite = OPPOSITES[face]
        verts_a = FACE_VERTICES[face]
        verts_b = FACE_VERTICES[opposite]
        for va, vb in zip(verts_a, verts_b):
            assert a.vertices[va] is b.vertices[vb], (
                f"Direction {face}: {va} IS {vb} failed"
            )


def test_shared_vertex_state_propagates():
    """Data processed on a shared vertex is visible from both cubes."""
    import asyncio
    a = Cube("a")
    b = Cube("b")
    connect_cubes(a, 'N', b)

    # Write state to shared vertex via cube_a
    shared_llm = a.vertices['NEU']
    shared_llm.b[0] = 99.0  # Modify bias directly

    # Read it from cube_b's touching vertex
    assert b.vertices['SEU'].b[0] == 99.0


# ============================================================
# RecursiveCube tests
# ============================================================

def test_recursive_cube_level_0():
    """Level-0 RecursiveCube wraps a single Cube."""
    rc = RecursiveCube(level=0, cube_id="leaf")
    assert rc.is_leaf()
    assert rc.cube is not None
    assert rc.corners is None
    assert rc.count_leaves() == 1
    assert rc.count_all_nodes() == 1


def test_recursive_cube_level_1():
    """Level-1 RecursiveCube has 8 leaf corners."""
    rc = RecursiveCube(level=1, cube_id="meta")
    assert not rc.is_leaf()
    assert len(rc.corners) == 8
    assert rc.count_leaves() == 8
    assert rc.count_all_nodes() == 9  # 8 leaves + 1 meta


def test_recursive_cube_level_3():
    """Level-3 RecursiveCube has 8^3 = 512 leaves."""
    rc = RecursiveCube(level=3, cube_id="deep")
    assert rc.count_leaves() == 8 ** 3
    assert rc.count_all_nodes() == sum(8 ** i for i in range(4))


def test_recursive_cube_get_face():
    """get_face() returns 4 corners at level N, Cube at level 0."""
    rc1 = RecursiveCube(level=1, cube_id="meta")
    n_face = rc1.get_face('N')
    assert len(n_face) == 4
    for corner in n_face:
        assert isinstance(corner, RecursiveCube)

    rc0 = RecursiveCube(level=0, cube_id="leaf")
    face = rc0.get_face('N')
    assert isinstance(face, Cube)


def test_recursive_cube_store_and_get():
    """Interior storage works at any level."""
    rc = RecursiveCube(level=2, cube_id="store-test")
    rc.store('era', 'Ancient Rome 110 CE')
    assert rc.get('era') == 'Ancient Rome 110 CE'
    assert rc.get('nonexistent') is None


def test_recursive_cube_walk_leaves():
    """walk_leaves() yields exactly count_leaves() nodes."""
    rc = RecursiveCube(level=2, cube_id="walk-test")
    leaves = list(rc.walk_leaves())
    assert len(leaves) == rc.count_leaves()
    assert all(leaf.is_leaf() for leaf in leaves)


def test_recursive_cube_connect_level_0():
    """connect() at level 0 shares FemtoLLM vertices."""
    a = RecursiveCube(level=0, cube_id="a")
    b = RecursiveCube(level=0, cube_id="b")
    a.connect(b, 'E')

    # East face of a: SED, NED, SEU, NEU
    # West face of b: SWD, NWD, SWU, NWU
    assert a.cube.vertices['SED'] is b.cube.vertices['SWD']
    assert a.cube.vertices['NEU'] is b.cube.vertices['NWU']


def test_recursive_cube_connect_level_1():
    """connect() at level 1 shares 4 corner sub-cubes."""
    a = RecursiveCube(level=1, cube_id="meta_a")
    b = RecursiveCube(level=1, cube_id="meta_b")
    a.connect(b, 'N')

    # North face corners of a: indices 2,3,6,7
    # South face corners of b: indices 0,1,4,5
    n_indices = FACE_CORNERS['N']  # [2, 3, 6, 7]
    s_indices = FACE_CORNERS['S']  # [0, 1, 4, 5]

    for ai, bi in zip(n_indices, s_indices):
        assert a.corners[ai] is b.corners[bi], (
            f"a.corners[{ai}] IS b.corners[{bi}] failed"
        )


def test_recursive_cube_winding_zero_after_connect():
    """winding_number() returns 0.0 for an adjacent connected pair."""
    a = RecursiveCube(level=1, cube_id="winding_a")
    b = RecursiveCube(level=1, cube_id="winding_b")
    a.connect(b, 'E')

    winding = a.winding_number([a, b])
    assert abs(winding) < 0.5, f"Expected near-zero winding, got {winding}"


def test_recursive_cube_same_level_required():
    """connect() raises ValueError when levels differ."""
    import pytest
    a = RecursiveCube(level=0, cube_id="leaf")
    b = RecursiveCube(level=1, cube_id="meta")
    try:
        a.connect(b, 'N')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
