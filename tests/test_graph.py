import pytest
from ee.hogai.graph import AssistantGraph
from ee.hogai.utils.types import AssistantNodeName

# A dummy team to use during testing.
class DummyTeam:
    pass

def test_compile_without_start_node_raises_exception():
    """
    Test that compiling an AssistantGraph without adding a start node
    raises a ValueError.
    """
    dummy_team = DummyTeam()
    graph = AssistantGraph(dummy_team)
    # Without a start node being added, compile should raise a ValueError.
    with pytest.raises(ValueError, match="Start node not added"):
        graph.compile()

def test_compile_full_graph_returns_compiled_graph():
    """
    Test that compile_full_graph builds and compiles the entire graph without errors.
    This ensures that all node addition methods as well as their conditional edge wiring
    work as expected together.
    """
    dummy_team = DummyTeam()
    graph = AssistantGraph(dummy_team)
    # Calling compile_full_graph will add all nodes/edges and compile the graph.
    compiled_graph = graph.compile_full_graph()
    # Assert that compiling the full graph returns an object (compiled state graph)
    assert compiled_graph is not None
