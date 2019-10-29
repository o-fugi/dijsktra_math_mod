import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def filter_dictionary(dictionary, callback):
    newDict = dict()
    for (key, value) in dictionary.items():
        if callback((key, value)):
            newDict[key] = value
    return newDict

def plot_graph(G):
    fig = plt.subplot()
    nx.draw(G, with_labels=True)
    labels = nx.get_edge_attributes(G,'key')
    print(labels)
# nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G))
    plt.show()

def bad_weather(G):
    edge_attributes = pd.DataFrame.from_dict(nx.get_edge_attributes(G, 'value'), orient='index', columns=['value'])
    edge_attributes = edge_attributes.reset_index()
    edge_attributes = edge_attributes.join(pd.DataFrame(edge_attributes['index'].tolist(), index=edge_attributes.index))
    edge_attributes['location0'] = edge_attributes[0]
    edge_attributes['location1'] = edge_attributes[1]

    node_attributes = pd.DataFrame.from_dict(nx.get_node_attributes(G, 'location'), orient='index', columns=['location'])
    node_attributes = node_attributes.reset_index()
    node_attributes['location0'] = node_attributes['index']

    edge_and_nodes = edge_attributes.merge(node_attributes, on='location0')
    node_attributes['location1'] = node_attributes['index']
    edge_and_nodes = edge_and_nodes.merge(node_attributes, on='location1')

    edge_and_nodes['edge_name'] = edge_and_nodes['index_x']
    edge_and_nodes.loc[(edge_and_nodes['location_x'] == 'outside') | (edge_and_nodes['location_y'] == 'outside'), 'value'] = 2 * edge_and_nodes['value']
    edge_and_nodes.index = edge_and_nodes['edge_name']
    edge_and_nodes = edge_and_nodes[['value']]

    new_dict = edge_and_nodes.T.to_dict()
    nx.set_edge_attributes(G, new_dict)
    print(nx.get_edge_attributes(G, 'value'))

    return G

if __name__=="__main__":
    fh=open("school_graph6.txt", 'rb')
    G=nx.read_gml(fh)

    G = bad_weather(G)

    # plot_graph(G)

    print("Enter the hallway of the starting classroom")
    starting_classroom = input()
    print("Enter the hallway of the ending classroom")
    ending_classroom = input()

    print(nx.dijkstra_path(G, starting_classroom, ending_classroom, weight='value'))
