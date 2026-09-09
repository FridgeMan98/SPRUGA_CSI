"""Unit tests verifying explicit routing tables from dijkstra.py and bellman_ford.py."""

import pytest
from src.graph import Graph
from src.dijkstra import dijkstra, DijkstraEngine, MinHeap
from src.bellman_ford import bellman_ford, BellmanFordEngine


def test_min_heap_operations():
    heap = MinHeap()
    heap.push(10.0, "A")
    heap.push(4.0, "B")
    heap.push(7.0, "C")

    cost, item = heap.pop()
    assert (cost, item) == (4.0, "B")

    heap.decrease_key("A", 2.0)
    cost, item = heap.pop()
    assert (cost, item) == (2.0, "A")


@pytest.fixture
def sample_network():
    g = Graph(directed=False)
    g.add_edge("A", "B", weight=4.0)
    g.add_edge("A", "C", weight=2.0)
    g.add_edge("B", "C", weight=1.0)
    g.add_edge("B", "D", weight=5.0)
    g.add_edge("C", "D", weight=8.0)
    return g


def test_dijkstra_explicit_routing_table(sample_network):
    routing_table = dijkstra(sample_network, "A")
    
    # Verify table schema: [Destination | Next Hop | Cost | Path]
    for row in routing_table:
        assert "Destination" in row
        assert "Next Hop" in row
        assert "Cost" in row
        assert "Path" in row

    # Target D row check: A -> C -> B -> D (Cost 8.0)
    d_row = next(r for r in routing_table if r["Destination"] == "D")
    assert d_row["Next Hop"] == "C"
    assert d_row["Cost"] == 8.0
    assert d_row["Path"] == ["A", "C", "B", "D"]


def test_bellman_ford_explicit_routing_table(sample_network):
    routing_table = bellman_ford(sample_network, "A")
    
    # Verify table schema: [Destination | Next Hop | Cost | Path]
    for row in routing_table:
        assert "Destination" in row
        assert "Next Hop" in row
        assert "Cost" in row
        assert "Path" in row

    # Target D row check: A -> C -> B -> D (Cost 8.0)
    d_row = next(r for r in routing_table if r["Destination"] == "D")
    assert d_row["Next Hop"] == "C"
    assert d_row["Cost"] == 8.0
    assert d_row["Path"] == ["A", "C", "B", "D"]


def test_bellman_ford_deep_topology_convergence():
    """Verify Bellman-Ford converges on deep topologies requiring V-1 iterations."""
    g = Graph(directed=False)
    # 6-node linear chain: N1 - N2 - N3 - N4 - N5 - N6
    nodes = ["N1", "N2", "N3", "N4", "N5", "N6"]
    for i in range(len(nodes) - 1):
        g.add_edge(nodes[i], nodes[i + 1], weight=1.0)

    routing_table = bellman_ford(g, "N1")
    n6_row = next(r for r in routing_table if r["Destination"] == "N6")
    assert n6_row["Cost"] == 5.0
    assert n6_row["Path"] == ["N1", "N2", "N3", "N4", "N5", "N6"]

