# ForkThis Master Bug Inventory & Solution Guide

This document tracks all intentional bugs injected for the **ForkThis** event, including location, symptoms, failure behavior, and exact solutions.

---

## Tier 2: Silent Logic Bugs

### Bug 2.1: Directional Link Mutator (Graph Logic)

- **Target File**: [`src/graph.py`](file:///c:/Users/aravi/Downloads/VIT_STUDIES/Comp_Netw/PROJECT_SPRUGA/SPRUGA_CSI/SPRUGA_CSI/src/graph.py#L38-L45)
- **Component**: `Graph.add_edge(u, v, weight)`
- **Symptom**:
  - In undirected graphs, forward neighbor queries (`U -> V`) report the correct edge cost (e.g. `5.0`), but reverse queries (`V -> U`) return `0.0`.
  - Routing algorithms (Dijkstra and Bellman-Ford) return incorrect lower costs (e.g. `7.0` instead of `8.0`) or incorrect reverse paths.
- **Failing Tests**:
  - `tests/test_graph.py::test_add_nodes_and_edges` (`assert g.get_neighbors("B")["A"] == 5.0` fails with `0.0 == 5.0`)
  - `tests/test_algorithms.py::test_dijkstra_explicit_routing_table` (`Cost 7.0 == 8.0`)
  - `tests/test_algorithms.py::test_bellman_ford_explicit_routing_table` (`Cost 7.0 == 8.0`)

#### Root Cause
In `add_edge()`, when `self.directed` is `False`, the reverse edge `$V \to U$` is assigned a hardcoded weight of `0.0` instead of `float(weight)`.

#### Buggy Code (`src/graph.py`):
```python
if not self.directed:
    # BUG 2.1: Reverse link V -> U hardcoded with cost 0.0
    self.adj[v][u] = {"weight": 0.0, "active": active}
```

#### Solution Patch:
```python
if not self.directed:
    self.adj[v][u] = {"weight": float(weight), "active": active}
```
