import pytest
from unittest.mock import MagicMock
from ee.hogai.graph import AssistantGraph, AssistantNodeName
from posthog.models.team.team import Team

def test_compile_without_start_node():
    """Test that compiling the graph without a start node added raises a ValueError."""
    # Create a dummy team using MagicMock
    team = MagicMock(spec=Team)
    graph = AssistantGraph(team)
    # Add a node that is not the START node; _has_start_node remains False
    graph.add_node(AssistantNodeName.QUERY_EXECUTOR, lambda x: x)
    with pytest.raises(ValueError, match="Start node not added to the graph"):
        graph.compile()
def test_compile_full_graph_successful():
    """Test that compile_full_graph successfully compiles a full graph and returns a valid object."""
    team = MagicMock(spec=Team)
    graph = AssistantGraph(team)
    # This should compile a full graph without errors
    compiled = graph.compile_full_graph()
    assert compiled is not None
def test_add_edge_start_sets_has_start():
    """Test that adding an edge from the START node sets the _has_start_node flag to True."""
    team = MagicMock(spec=Team)
    graph = AssistantGraph(team)
    # Initially, _has_start_node should be False
    assert not graph._has_start_node
    # Add an edge from the START node; this should set _has_start_node to True.
    graph.add_edge(AssistantNodeName.START, AssistantNodeName.QUERY_EXECUTOR)
    assert graph._has_start_node