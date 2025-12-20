from utils.inputs import get_inputs


def parse_devices(data):
    devices = {}
    for line in data:
        source, dest = line.split(":")
        devices[source] = set(dest.strip().split(' '))
    return devices


def find_paths(devices, start, end):
    todo = [[start]]
    paths = []
    while todo:
        path = todo.pop(0)
        node = path[-1]

        for output in devices.get(node, []):
            if output in path:
                print(f"sneaky loop found {output} -> {path}")
                continue
            new_path = list(path) + [output]
            if output == end:
                paths.append(new_path)
            else:
                todo.append(new_path)
    print(f"found {len(paths)} paths")
    return paths


def part_one(data):
    devices = parse_devices(data)

    return len(find_paths(devices, 'you', 'out'))


def part_two(data):
    devices = parse_devices(data)
    import networkx as nx
    import plotly.graph_objects as go

    G = nx.DiGraph()

    edges = []
    for k, l in devices.items():
        for ll in l:
            edges.append((k, ll))
    G.add_edges_from(edges)
    pos = nx.circular_layout(G)

    graph1 = {
        'graph': {
            'directed': True,
            'nodes': {},
            'edges': []
        }
    }
    for k, l in devices.items():
        graph1['graph']['nodes'][k] = {}
        for ll in l:
            graph1['graph']['edges'].append({'source': k, 'target': ll})

    data = {
        'graph': {
            'directed': False,
            'nodes': {
                1: {},
                2: {},
                3: {},
            },
            'edges': [
                {'source': 1, 'target': 2},
                {'source': 2, 'target': 3},
            ]
        }
    }
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="bottom center",
        marker=dict(
            showscale=False,
            size=20,
            color='#2ca02c',
            line_width=2))

    # 5. Create the figure and add annotations for arrows
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Directed Acyclic Graph (DAG) Example with Plotly and NetworkX',
                        # titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[
                            dict(
                                ax=pos[edge[0]][0], ay=pos[edge[0]][1], axref='x', ayref='y',
                                x=pos[edge[1]][0], y=pos[edge[1]][1], xref='x', yref='y',
                                showarrow=True,
                                arrowhead=2,  # Creates an arrow
                                arrowsize=1,
                                arrowwidth=1,
                                opacity=0.6
                            ) for edge in G.edges()
                        ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()

    # fig = gv.d3(graph1, use_node_size_normalization=True, node_size_normalization_max=30,
    #            use_edge_size_normalization=True, edge_size_data_source='weight', edge_curvature=0.3)
    # fig.export_svg('todo.svg')
    # fig.export_html('graph2.html')
    # import scipy

    # plt.tight_layout()
    # plt.constrained_layout()
    # nx.draw_networkx(graph, arrows=True)
    # graph = nx.nx_agraph.to_agraph(dag)
    # graph.draw("g1.svg", prog="dot")
    # plt.savefig("g1.svg", format="SVG")
    # tell matplotlib you're done with the plot: https://stackoverflow.com/questions/741877/how-do-i-tell-matplotlib-that-i-am-done-with-a-plot
    # plt.clf()
    # dac_paths = find_paths(devices, 'dac', 'out')
    # fft_paths = find_paths(devices, 'fft', 'out')
    # print(len(dac_paths), len(fft_paths))
    # svr_dac_paths = find_paths(devices, 'svr', 'dac')
    # svr_fft_paths = find_paths(devices, 'svr', 'fft')
    # print(len(svr_dac_paths), len(svr_fft_paths))
    # return len(list(filter(lambda path: 'dac' in path and 'fft' in path, find_paths(devices, 'svr'))))


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_two,):
        # print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
