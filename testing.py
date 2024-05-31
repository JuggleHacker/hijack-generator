import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


def testing(number_of_nodes):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    G=nx.Graph()
    for i in range(number_of_nodes):
        G.add_node(str(i+1))
    for i in range(number_of_nodes):
        G.add_edge(str(i+1),str((i+1)%number_of_nodes+1))
    pos=nx.spring_layout(G)
    val_map = {str(i):i for i in range(1,number_of_nodes+1)}
    ColorLegend = {str(i+1)+': '+alphabet[i]:i+1 for i in range(number_of_nodes)}
    values = [val_map.get(node, 0) for node in G.nodes()]

    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=max(values))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    # Using a figure to use it as a parameter when calling nx.draw_networkx
    f = plt.figure(1)
    ax = f.add_subplot(1,1,1)
    for my_label in ColorLegend:
        ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[my_label]),label=my_label)

    # Just fixed the color map
    nx.draw_networkx(G,pos, cmap = jet,node_color=values,with_labels=True,ax=ax)

    # Setting it to how it was looking before.
    plt.axis('off')
    f.set_facecolor('w')

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, mode="expand", borderaxespad=0.)

    f.tight_layout()
    plt.savefig("network"+str(number_of_nodes)+".png")
    plt.close()
