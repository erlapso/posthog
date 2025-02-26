import pytest
from unittest.mock import MagicMock

from ee.hogai.graph import AssistantGraph
from ee.hogai.utils.types import AssistantNodeName

def test_compile_without_start_node():
    """Test that compiling an AssistantGraph without a start node raises a ValueError."""
    dummy_team = MagicMock()
    graph = AssistantGraph(dummy_team)
    # Since we haven't added any start node, compile() should raise a ValueError.
    with pytest.raises(ValueError, match="Start node not added to the graph"):
            graph.compile()
def test_compile_with_start_node():
    """Test that compiling an AssistantGraph with a start node properly set returns a compiled graph."""
    dummy_team = MagicMock()
    graph = AssistantGraph(dummy_team)
    # Add an edge from START to QUERY_EXECUTOR so that _has_start_node becomes True.
    graph.add_edge(AssistantNodeName.START, AssistantNodeName.QUERY_EXECUTOR)
    # Add dummy nodes for START and QUERY_EXECUTOR to satisfy the compile process.
    dummy_action = MagicMock()
    graph.add_node(AssistantNodeName.QUERY_EXECUTOR, dummy_action)
    compiled_graph = graph.compile()
    assert compiled_graph is not None
def test_compile_full_graph():
    """Test that compiling a fully assembled AssistantGraph returns a compiled graph."""
    dummy_team = MagicMock()
    graph = AssistantGraph(dummy_team)
    compiled_graph = graph.compile_full_graph()
    assert compiled_graph is not None