import pytest
from unittest.mock import MagicMock
from ee.hogai.graph import AssistantGraph, AssistantNodeName
from posthog.models.team.team import Team

def test_compile_without_start_node_raises_error():
    """Test that compiling the graph without a start node raises a ValueError."""
    dummy_team = MagicMock(spec=Team)
    graph = AssistantGraph(dummy_team)
    # Do not add any node or edge that would mark the start node
    with pytest.raises(ValueError, match="Start node not added to the graph"):
        graph.compile()
def test_compile_full_graph_success():
    """Test that compiling the complete graph builds a non-null graph structure."""
    dummy_team = MagicMock(spec=Team)
    graph = AssistantGraph(dummy_team)
    # Build the full graph by chaining all node additions and compile it.
    compiled_graph = graph.compile_full_graph()
    # Assert that the compiled graph is returned successfully (i.e. it is not None).
    assert compiled_graph is not None
def test_add_edge_marks_start_node():
    """Test that adding an edge from the START node marks _has_start_node and allows compile to succeed."""
    dummy_team = MagicMock(spec=Team)
    graph = AssistantGraph(dummy_team)
    # Add an edge from START so that _has_start_node is set to True
    graph.add_edge(AssistantNodeName.START, AssistantNodeName.ROOT)
    graph.add_node(AssistantNodeName.ROOT, MagicMock())
    # Assert that the internal flag is set
    assert graph._has_start_node is True
    # Add a dummy node required for compile to complete (if needed by the StateGraph)
    graph.add_node(AssistantNodeName.QUERY_EXECUTOR, MagicMock())
    # Now compile should succeed and return a non-None compiled graph
    compiled = graph.compile()
    assert compiled is not None