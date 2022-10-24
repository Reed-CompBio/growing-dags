import sys
import networkx as nx
import glob
import numpy as np
import matplotlib.pyplot as plt

PL_NODES = {}
PL_EDGES = {}
C1_NODES = {}
C2_NODES = {}
C1_EDGES = {}
C2_EDGES = {}

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
COLORS = {'C1':'#6AB1E2','C2':'#376A1D','PL':'#DD8C54'}
NAMES = {'TGFbetaReceptor':'TGF_beta_Receptor'}
NUM_NODES = {'BCR':137,'EGFR1':231,'IL1':43,'TCR':154,'TGFbetaReceptor':209,'Wnt':106}
NUM_EDGES = {'BCR':456,'EGFR1':1456,'IL1':178,'TCR':504,'TGFbetaReceptor':863,'Wnt':428}

def main():
    global PL_NODES,PL_EDGES,C1_NODES,C2_NODES,C1_EDGES,C2_EDGES

    for label in PATHWAYS:
        print('label:',label)
        print('GT PL C1 C2')

        PL_NODES[label] = get_output(label,'PL','nodes')
        C1_NODES[label] = get_output(label,'c1','nodes')
        C2_NODES[label] = get_output(label,'c2','nodes')
        print(NUM_NODES[label],PL_NODES[label][-1],C1_NODES[label][-1],C2_NODES[label][-1])

        PL_EDGES[label] = get_output(label,'PL','edges')
        C1_EDGES[label] = get_output(label,'c1','edges')
        C2_EDGES[label] = get_output(label,'c2','edges')

    make_node_plot()
    make_edge_plot()

def make_node_plot():

    ## NODES FIRST
    fig, axes = plt.subplots(2,3,figsize=(12,8))
    for i,ax in enumerate(axes.flat):
        p = PATHWAYS[i]
        print(i,p)

        #PL
        x1,y1,max1 = get_data_for_plot(PL_NODES[p])
        ax.plot(x1,y1,linewidth=3,marker='o',linestyle='-', color=COLORS['PL'],alpha=0.8,label='PathLinker (k=%d)' % (max1))

        x2,y2,max2 = get_data_for_plot(C1_NODES[p])
        ax.plot(x2,y2,linewidth=3,marker='s',linestyle='-', color=COLORS['C1'],alpha=0.8,label='DAG $c_1$ (k=%d)' % (max2))

        x3,y3,max3 = get_data_for_plot(C2_NODES[p])
        ax.plot(x3,y3,linewidth=3,marker='d',linestyle='-', color=COLORS['C2'],alpha=0.8,label='DAG $c_2$ (k=%d)' % (max3))

        ax.plot([0,max(max1,max2,max3)],[NUM_NODES[p],NUM_NODES[p]],'--k',label='Ground Truth')

        ax.legend()
        ax.set_title('%s Nodes' % (p))
        ax.set_xlabel('Iteration $k$')
        ax.set_ylabel('# Nodes')
    plt.tight_layout()
    plt.savefig('nodes_final.png')
    print('saved to nodes_final.png')
    plt.savefig('nodes_final.pdf')
    print('saved to nodes_final.pdf')

    return

def make_edge_plot():
    plt.clf()
    fig, axes = plt.subplots(2,3,figsize=(12,8))
    for i,ax in enumerate(axes.flat):
        p = PATHWAYS[i]
        print(i,p)

        #PL
        x1,y1,max1 = get_data_for_plot(PL_EDGES[p])
        ax.plot(x1,y1,linewidth=3,marker='o',linestyle='-', color=COLORS['PL'],alpha=0.8,label='PathLinker (k=%d)' % (max1))

        x2,y2,max2 = get_data_for_plot(C1_EDGES[p])
        ax.plot(x2,y2,linewidth=3,marker='s',linestyle='-', color=COLORS['C1'],alpha=0.8,label='DAG $c_1$ (k=%d)' % (max2))

        x3,y3,max3 = get_data_for_plot(C2_EDGES[p])
        ax.plot(x3,y3,linewidth=3,marker='d',linestyle='-', color=COLORS['C2'],alpha=0.8,label='DAG $c_2$ (k=%d)' % (max3))
        ax.plot([0,max(max1,max2,max3)],[NUM_EDGES[p],NUM_EDGES[p]],'--k',label='Ground Truth')

        ax.legend()
        ax.set_title('%s Edges' % (p))
        ax.set_xlabel('Iteration $k$')
        ax.set_ylabel('# Edges')
    plt.tight_layout()
    plt.savefig('edges_final.png')
    print('saved to edges_final.png')
    plt.savefig('edges_final.pdf')
    print('saved to edges_final.pdf')

    return

def get_data_for_plot(vals):
    inds = list(range(0,len(vals),int(len(vals)/20)))+[len(vals)-1]
    x = [vals[i][1] for i in inds]
    y = [vals[i][0] for i in inds]
    #print(x)
    #print(y)
    #sys.exit()
    return x,y,vals[-1][1]

def get_output(label,c,nodes_or_edges):
    G_STATS = []
    GROWING_G = nx.DiGraph()
    if c != 'PL':
        G0_file = '../../data/prepare-G0/pathlinker/%s-G0.txt' % (label)
        #print('  ',G0_file)
        with open(G0_file) as fin:
            for line in fin:
                row = line.strip().split()
                GROWING_G.add_edge(row[0],row[1])
        G_STATS.append([get_stats(GROWING_G,nodes_or_edges),0]) #G0

    G_STATS_file = '../../output/pathlinker-final/%s_%s_%s.txt' % (label,c,nodes_or_edges)
    #print('  ',G_STATS_file)
    with open(G_STATS_file) as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            if c == 'PL':
                GROWING_G.add_edge(row[0],row[1])
                G_STATS.append([get_stats(GROWING_G,nodes_or_edges),int(row[2])])
            else:
                path = row[2].split('|')
                nx.add_path(GROWING_G,path)
                G_STATS.append([get_stats(GROWING_G,nodes_or_edges),int(row[0])])
    #print(c,G_STATS[-1])
    return G_STATS

def get_stats(G,nodes_or_edges):
    if nodes_or_edges == 'nodes':
        return G.number_of_nodes()
    else:
        return G.number_of_edges()

if __name__ == '__main__':
    main()
