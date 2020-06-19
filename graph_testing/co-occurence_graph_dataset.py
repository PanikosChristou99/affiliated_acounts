import os
import re

import matplotlib.pyplot as plt
import networkx as nx


def create_data_test_from_target(target):
    regex_mention = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_.]))@([A-Za-z]+[A-Za-z0-9-_]+)')

    G = nx.Graph()

    training_data_location = os.path.join('D:/affiliated_acounts', 'Data', 'stance-data',
                                          'data-all-annotations', 'trainingdata-all-annotations.txt')
    file1 = open(training_data_location, 'r')
    lines = file1.readlines()[1:]
    # print(lines)
    lines_tokenized = [line.split() for line in lines]
    # print(lines_tokenized)
    target_tokenized = target.split()
    # print(target_tokenized)
    collumns_of_target = [line_tokenized[1: len(target_tokenized) + 1] for line_tokenized in lines_tokenized]

    # a list of lists that have all  collumns that should contain target else its something we dont need

    # print(collumns_of_target)

    # 1007	Climate Change is a Real Concern	If we do not act, we wi
    # 1008	Climate Change is a Real Concern	The carbon clock is tic
    # 1009	Feminist Movement	Always a delight to see chest-drumming
    # 1010	Feminist Movement	Sometimes I overheat and want to take o

    # here tagret feminist movemnt is 2 collumns but its perivious is 4 so  it will think that "is a" is text of it

    data = [lines_tokenized[i][len(target_tokenized) + 1:-4] for i in range(len(lines)) if
            collumns_of_target[i] == target_tokenized]
    print(data)
    data = data[:100]
    # df = pd.DataFrame(data)
    # df.to_csv("./final_data.csv", sep=' ', index=False)
    target_no_spaces = target.replace(" ", "")
    for line_tokenized in data:
        for token in line_tokenized:
            match = re.findall(regex_mention, token)
            if match and match[0] != target_no_spaces:
                if G.has_edge(target, match[0]):
                    G.add_edge(target, match[0],
                               weight=G[target][match[0]]['weight'] + 1)
                else:
                    G.add_edge(target, match[0], weight=1)

    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif')
    nx.draw(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


create_data_test_from_target('Hillary Clinton')
#
# # labels
#
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw(G,pos)
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
# plt.axis('off')
# plt.savefig("weighted_graph.png") # save as png
# plt.show() # display
