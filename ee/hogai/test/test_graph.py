import pytest
from ee.hogai.graph import AssistantGraph
from ee.hogai.utils.types import AssistantNodeName, AssistantState

# Dummy team for testing purposes
class DummyTeam:
    pass

@pytest.fixture
def team():
    """Fixture to return a dummy team instance."""
    return DummyTeam()

@pytest.fixture
def assistant_graph(team):
    """Fixture to construct an AssistantGraph with a dummy team."""
    return AssistantGraph(team)

def test_compile_without_start_node(assistant_graph):
    """
    Test that compiling the graph without a start node raises a ValueError.
    """
    with pytest.raises(ValueError, match="Start node not added to the graph"):
        assistant_graph.compile()

def test_add_edge_sets_start_node(assistant_graph):
    """
    Test that adding an edge from the START node sets the _has_start_node flag.
    """
    # Add edge from START and to an arbitrary node (e.g., ROOT)
    assistant_graph.add_edge(AssistantNodeName.START, AssistantNodeName.ROOT)
    # Add a dummy action for the ROOT node required for compilation.
    assistant_graph.add_node(AssistantNodeName.ROOT, lambda x: x)
    compiled = assistant_graph.compile()
    assert compiled is not None

def test_full_graph_compilation(assistant_graph):
    """
    Test that chaining all graph methods via compile_full_graph returns a compiled graph.
    """
    compiled = assistant_graph.compile_full_graph()
    assert compiled is not None

def test_memory_initializer_sets_start_flag(assistant_graph):
    """
    Test that the memory initializer adds the start node flag.
    """
    # Initially, _has_start_node should be False
    assert not assistant_graph._has_start_node
    assistant_graph.add_memory_initializer()
    # After calling add_memory_initializer, _has_start_node is set to True
    assert assistant_graph._has_start_node

def test_add_root_does_not_fail(assistant_graph):
    """
    Test that calling add_root (with its default path_map) correctly adds nodes
    and does not raise any exceptions once a start node is added.
    """
    # Ensure we have at least one start node.
    assistant_graph.add_edge(AssistantNodeName.START, AssistantNodeName.ROOT)
    # Call add_root to add ROOT and ROOT_TOOLS nodes and conditional edges.
    # Use a custom path_map that only references nodes present in the test to avoid unknown nodes
    assistant_graph.add_root(path_map={
        "trends": AssistantNodeName.ROOT,
        "funnel": AssistantNodeName.ROOT,
        "retention": AssistantNodeName.ROOT,
        "root": AssistantNodeName.ROOT,
        "end": AssistantNodeName.END,
    })
    compiled = assistant_graph.compile()
    assert compiled is not None