"""Configuration for testing

The configuration file provides several default graph fixtures
and test functions

1. `standard_G` - test graph generated using DiGraph, scope: function
2. `mmodel_G` - test graph generated using ModelGraph. scope: function
"""


import pytest
from inspect import signature, Signature, Parameter
import networkx as nx
from mmodel.graph import ModelGraph
import math
from networkx.utils import nodes_equal, edges_equal


@pytest.fixture()
def standard_G():
    """Standard test graph generated using DiGraph

    The result is:
    k = (a + b - d)(a + b)f
    m = log(a + b, b)
    """

    def addition(a, b=2):
        return a + b

    def subtraction(c, d):
        return c - d

    def multiplication(c, f):
        return c * f

    def polynomial(e, g):
        return e * g

    def logarithm(c, b):
        return math.log(c, b)

    node_list = [
        ("add", {"func": addition, "returns": ["c"], "sig": signature(addition)}),
        (
            "subtract",
            {"func": subtraction, "returns": ["e"], "sig": signature(subtraction)},
        ),
        (
            "multiply",
            {
                "func": multiplication,
                "returns": ["g"],
                "sig": signature(multiplication),
            },
        ),
        ("poly", {"func": polynomial, "returns": ["k"], "sig": signature(polynomial)}),
        ("log", {"func": logarithm, "returns": ["m"], "sig": signature(logarithm)}),
    ]

    edge_list = [
        ("add", "subtract", {"val": ["c"]}),
        ("subtract", "poly", {"val": ["e"]}),
        ("add", "multiply", {"val": ["c"]}),
        ("multiply", "poly", {"val": ["g"]}),
        ("add", "log", {"val": ["c"]}),
    ]

    G = nx.DiGraph(name="test", doc="test object\n\nlong description")
    G.graph["type"] = "ModelGraph"  # for comparison

    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)

    return G


@pytest.fixture()
def mmodel_G():
    """Mock test graph generated using ModelGraph

    The result is:
    k = (a + b - d)(a + b)f
    m = log(a + b, b)
    """

    def addition(a, b=2):
        return a + b

    def subtraction(c, d):
        return c - d

    def multiplication(c, f):
        return c * f

    def polynomial(e, g):
        return e * g

    def logarithm(c, b):
        return math.log(c, b)

    doc = "test object\n\nlong description"

    grouped_edges = [
        ("add", ["subtract", "multiply", "log"]),
        (["subtract", "multiply"], "poly"),
    ]

    node_objects = [
        ("add", addition, ["c"]),
        ("subtract", subtraction, ["e"]),
        ("multiply", multiplication, ["g"]),
        ("poly", polynomial, ["k"]),
        ("log", logarithm, ["m"]),
    ]

    G = ModelGraph(name="test", doc=doc)
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)
    return G


@pytest.fixture(scope="module")
def mmodel_signature():
    """The default signature of the mmodel_G models"""

    param_list = [
        Parameter("a", 1),
        Parameter("d", 1),
        Parameter("f", 1),
        Parameter("b", 1, default=2),
    ]

    return Signature(param_list)


def graph_equal(G1, G2):
    """Test if graphs have the same nodes, edges and attributes"""

    assert nodes_equal(G1._node, G2._node)
    assert edges_equal(G1._adj, G2._adj)

    assert G1._pred == G2._pred
    assert G1._succ == G2._succ

    # test graph attributes
    assert G1.graph == G2.graph
    assert G1.name == G2.name

    return True
