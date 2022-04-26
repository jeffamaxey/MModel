import graphviz
from copy import deepcopy

DEFAULT_SETTINGS = {
    "graph_attr": {
        "labelloc": "t",
        "labeljust": "l",
        "splines": "ortho",
        "ordering": "out",
    },
    "node_attr": {"shape": "box"},
}


def update_settings(label):
    """Update graphviz settings

    Creates a copy of the default dictionary
    and update the graph label in graph attribute
    """

    # copy() is shallow, does not copy the nested dict
    new_settings = deepcopy(DEFAULT_SETTINGS)
    new_settings["graph_attr"].update({"label": label})

    return new_settings


def draw_plain_graph(G, label=""):
    """Draw plain graph

    :param str name: name of the graph
    :param str label: title of the graph

    Plain graph contains the graph label (name + doc)
    Each node only shows the node name
    """

    settings = update_settings(label)
    dot_graph = graphviz.Digraph(name=G.name, **settings)

    for node in G.nodes:
        dot_graph.node(node)

    for u, v in G.edges:
        dot_graph.edge(u, v)

    return dot_graph



def draw_graph(G, label=""):
    """Draw detailed graph

    :param str name: name of the graph
    :param str label: title of the graph

    Plain graph contains the graph label (name + doc + input + output)
    Each node shows node label (name + signature + returns)

    Subgraph node shows the label and subgraph doc.
    """

    settings = update_settings(label)

    dot_graph = graphviz.Digraph(name=G.name, **settings)

    for node, ndict in G.nodes(data=True):

        if "obj" in ndict:
            label = (
                f"{node}\l\n{ndict['obj'].__name__}"
                f"{ndict['sig']}\lreturn {', '.join(ndict['rts'])}\l"
            )
        else:
            label = node
        dot_graph.node(node, label=label)

    for u, v, edict in G.edges(data=True):

        if "val" in edict:
            xlabel = ", ".join(edict["val"])
        else:
            xlabel = ""

        dot_graph.edge(u, v, xlabel=xlabel)

    # temperarily disable subgraph plotting
    # for node, subgraph in nx.get_node_attributes(G, "subgraph").items():

    #     # use short docstring for subgraph
    #     dot_subgraph = draw_graph(subgraph, label=f"{node}", name=f"cluster {node}")
    #     dot_graph.subgraph(dot_subgraph)

    return dot_graph


