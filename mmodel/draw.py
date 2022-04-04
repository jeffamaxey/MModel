import graphviz


def draw_graph(G, name=None, show_detail=True, filename=None, **kwargs):
    """Show model graph

    The process create a graphviz graph and write networkx.graph
    nodes and edges to it.

    :param str title: title of the graph
    :param bool show_detail: default to true, all nodes signature
        and returns are shown.

    Optional dot graph settings can be suplied using additional
    keyword arguments - graph_attr, node_attr, and edge_attr.
    See graphviz dot file documentation for detailed customization.
    The original setting is completely replaced. Note the title
    (graph label) should be included in "graph_attr".

    """

    name = name or G.name
    doc = G.graph.get('doc', '')
    filename = filename or f"{name}.gv"
    default_settings = {
        "graph_attr": {
            "labelloc": "t",
            "splines": "ortho",
            "ordering": "out",
        },
        "node_attr": {"shape": "box"},
    }

    settings = {**default_settings, **kwargs}
    settings["graph_attr"]["label"] = f"{name}\n{doc}"

    dot_graph = graphviz.Digraph(name=name, filename=filename, **settings)

    dot_subgraphs = []

    for node, ndict in G.nodes(data=True):
        if ndict.get("has_subgraph", False):
            dot_subgraphs.append([node, ndict])

        if show_detail:
            rts = ", ".join(ndict["return_params"])
            label = f"{node}\l\n{ndict['node_obj'].__name__}{ndict['signature']}\lreturn {rts}\l"
            dot_graph.node(node, label=label)
        else:
            dot_graph.node(node)

    for u, v, edict in G.edges(data=True):
        if show_detail:
            dot_graph.edge(u, v, xlabel=" ".join(edict["interm_params"]))
        else:
            dot_graph.edge(u, v)

    # draw subgraph if there is any
    for node, ndict in dot_subgraphs:
        node_obj = ndict["node_obj"]
        subgraph = node_obj.G
        title = node
        dot_sub = draw_graph(
            subgraph, name=f"cluster_{title}", show_detail=show_detail, **kwargs
        )
        dot_graph.subgraph(dot_sub)

    return dot_graph
