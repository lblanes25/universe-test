"""Focal selection via Louvain communities on the undirected handoff graph.

Each active entity is assigned to exactly one batch as 'focal'. Batches
target `K` focal entities. Communities larger than K are subdivided;
communities smaller than K/2 are merged with the closest neighbor.
Isolated entities (no handoffs) form a trailing 'isolated' batch.
"""
from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import pandas as pd
from networkx.algorithms.community import louvain_communities


@dataclass
class FocalBatch:
    batch_id: int
    focal_ids: list[str]
    isolated: bool = False


def build_undirected_handoff_graph(nodes: pd.DataFrame, handoffs: pd.DataFrame) -> nx.Graph:
    active_ids = set(nodes["Audit Entity ID"])
    G = nx.Graph()
    for aid in sorted(active_ids):  # deterministic node order
        G.add_node(aid)
    if handoffs.empty:
        return G
    valid = handoffs[
        (~handoffs["Unmatched"].astype(bool))
        & handoffs["Source Entity ID"].isin(active_ids)
        & handoffs["Target Entity ID"].isin(active_ids)
    ]
    # Deterministic edge order: sort endpoints
    edges = sorted(
        {tuple(sorted((r["Source Entity ID"], r["Target Entity ID"]))) for _, r in valid.iterrows()}
    )
    G.add_edges_from(edges)
    return G


def _arbitrary_chunk(xs: list[str], K: int) -> list[list[str]]:
    """Chunk into groups of K, but fold a trailing orphan (< K/2) into the prior chunk."""
    chunks = [xs[i:i + K] for i in range(0, len(xs), K)]
    floor = max(1, K // 2)
    if len(chunks) >= 2 and len(chunks[-1]) < floor:
        tail = chunks.pop()
        chunks[-1].extend(tail)
    return chunks


def _split_oversized(community: list[str], K: int, G: nx.Graph, seed: int) -> list[list[str]]:
    """Split a community larger than K into sub-communities of ~K using higher-resolution Louvain."""
    subg = G.subgraph(community).copy()
    if subg.number_of_edges() == 0:
        return _arbitrary_chunk(community, K)
    resolution = 1.0
    sub = [list(c) for c in louvain_communities(subg, seed=seed, resolution=resolution)]
    while any(len(s) > K for s in sub) and resolution < 8.0:
        resolution *= 1.5
        sub = [list(c) for c in louvain_communities(subg, seed=seed, resolution=resolution)]
    out: list[list[str]] = []
    for s in sub:
        if len(s) <= K:
            out.append(s)
        else:
            out.extend(_arbitrary_chunk(s, K))
    return out


def _merge_undersized(
    communities: list[list[str]], K: int, G: nx.Graph
) -> list[list[str]]:
    """Merge communities smaller than K/2 into the best neighbor.

    Preference order: (1) highest edge count; (2) if no edges to any eligible
    neighbor, the smallest community with room. Ensures size-1 orphans get folded.
    """
    floor = max(1, K // 2)
    communities = [sorted(c) for c in communities]
    changed = True
    while changed:
        changed = False
        for i, c in enumerate(communities):
            if len(c) >= floor:
                continue
            best_by_edge: tuple[int, int] | None = None  # (weight, j)
            best_by_size: tuple[int, int] | None = None  # (other_size, j)
            for j, other in enumerate(communities):
                if i == j:
                    continue
                if len(other) + len(c) > K:
                    continue
                w = sum(1 for u in c for v in other if G.has_edge(u, v))
                if best_by_edge is None or w > best_by_edge[0]:
                    best_by_edge = (w, j)
                if best_by_size is None or len(other) < best_by_size[0]:
                    best_by_size = (len(other), j)
            pick_j = None
            if best_by_edge and best_by_edge[0] > 0:
                pick_j = best_by_edge[1]
            elif best_by_size is not None:
                pick_j = best_by_size[1]
            if pick_j is not None:
                communities[pick_j] = sorted(communities[pick_j] + c)
                communities.pop(i)
                changed = True
                break
    return communities


def select_focal_batches(
    nodes: pd.DataFrame,
    handoffs: pd.DataFrame,
    focal_per_batch: int = 10,
    resolution: float = 1.0,
    seed: int = 42,
) -> list[FocalBatch]:
    G = build_undirected_handoff_graph(nodes, handoffs)
    # Separate isolated nodes
    isolated = [n for n, deg in G.degree() if deg == 0]
    connected_G = G.subgraph([n for n in G.nodes if n not in isolated]).copy()

    raw_communities: list[list[str]] = []
    ccs = sorted((sorted(cc) for cc in nx.connected_components(connected_G)), key=lambda x: (-len(x), x))
    for cc in ccs:
        sub = connected_G.subgraph(cc).copy()
        if len(cc) <= focal_per_batch:
            raw_communities.append(list(cc))
            continue
        if sub.number_of_edges() == 0:
            raw_communities.extend(_arbitrary_chunk(list(cc), focal_per_batch))
            continue
        communities = [sorted(c) for c in louvain_communities(sub, seed=seed, resolution=resolution)]
        communities.sort(key=lambda x: (-len(x), x))
        for c in communities:
            if len(c) > focal_per_batch:
                raw_communities.extend(_split_oversized(c, focal_per_batch, sub, seed))
            else:
                raw_communities.append(c)

    merged = _merge_undersized(raw_communities, focal_per_batch, connected_G)

    batches = [FocalBatch(batch_id=i + 1, focal_ids=sorted(c)) for i, c in enumerate(merged)]
    if isolated:
        batches.append(FocalBatch(batch_id=len(batches) + 1, focal_ids=sorted(isolated), isolated=True))
    return batches


def severed_edge_count(G: nx.Graph, batches: list[FocalBatch]) -> int:
    """Count handoff edges whose two endpoints are focal in different batches.

    Still covered by target/source context, but useful telemetry for batch composition.
    """
    entity_to_batch: dict[str, int] = {}
    for b in batches:
        for eid in b.focal_ids:
            entity_to_batch[eid] = b.batch_id
    severed = 0
    for u, v in G.edges():
        if entity_to_batch.get(u) != entity_to_batch.get(v):
            severed += 1
    return severed
