import sys
import networkx as nx
import glob
import numpy as np
import matplotlib.pyplot as plt

PL = {}
C1 = {}
C2 = {}
GT = {}

COLORS = {'c1':'#6AB1E2','c2':'#376A1D','PL':'#DD8C54'}
NAMES = {'TGFbetaReceptor':'TGF_beta_Receptor'}
NUM_NODES = {'BCR':137,'EGFR1':231,'IL1':43,'TCR':154,'TGFbetaReceptor':209,'Wnt':106}
NUM_EDGES = {'BCR':456,'EGFR1':1456,'IL1':178,'TCR':504,'TGFbetaReceptor':863,'Wnt':428}

def main(labels,k,costs):
    global PL,C1,C2
    print('labels:',labels)

    for label in labels:
        print('Running label:',label)
        PL[label] = get_PL_output(label,999)
        C1[label] = get_DAG_output(label,k,'c1')
        C2[label] = get_DAG_output(label,k,'c2')
        GT[label] = get_GT_output(label)

        print('\tNodes Edges Triangles')
        print('\tGT:',GT[label])
        print('\tPL:',PL[label][-1])
        print('\tC1:',C1[label][-1])
        print('\tC2:',C2[label][-1])

    make_plots(labels,k)

def make_plots(labels,k):
    global PL,C1,C2
    PL_means = []
    C1_means = []
    C2_means = []
    PL_std = []
    C1_std = []
    C2_std = []

    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7,4))

    # get average and stddev.
    for i in range(len(PL[labels[0]])):
        PL_means.append([np.mean([PL[l][i][0] for l in labels]),np.mean([PL[l][i][1] for l in labels]),np.mean([PL[l][i][2] for l in labels])])
        PL_std.append([np.std([PL[l][i][0] for l in labels]),np.std([PL[l][i][1] for l in labels]),np.std([PL[l][i][2] for l in labels])])

    x,y,y_err = get_data_for_plot(PL_means,PL_std,0)
    ax1.errorbar(x,y,yerr=y_err,elinewidth=1,linewidth=3,marker='o',linestyle='-',color=COLORS['PL'],alpha=0.8,label='PathLinker')
    PL_x_range = max(x)
    x,y,y_err = get_data_for_plot(PL_means,PL_std,1)
    ax2.errorbar(x,y,yerr=y_err,elinewidth=1,linewidth=3,marker='o',linestyle='-',color=COLORS['PL'],alpha=0.8,label='PathLinker')

    for i in range(len(C1[labels[0]])):
        C1_means.append([np.mean([C1[l][i][0] for l in labels]),np.mean([C1[l][i][1] for l in labels]),np.mean([C1[l][i][2] for l in labels])])
        C1_std.append([np.std([C1[l][i][0] for l in labels]),np.std([C1[l][i][1] for l in labels]),np.std([C1[l][i][2] for l in labels])])
        #print('C1',i,C1_means[i],'from',[C1[l][i] for l in labels])
    x,y,y_err = get_data_for_plot(C1_means,C1_std,0)
    ax1.errorbar(x,y,yerr=y_err,elinewidth=1,linewidth=3,marker='s',linestyle='-',color=COLORS['c1'],alpha=0.8,label='DAG $c_1$')
    x,y,y_err = get_data_for_plot(C1_means,C1_std,1)
    ax2.errorbar(x,y,yerr=y_err,elinewidth=1,linewidth=3,marker='s',linestyle='-',color=COLORS['c1'],alpha=0.8,label='DAG $c_1$')

    for i in range(len(C2[labels[0]])):
        C2_means.append([np.mean([C2[l][i][0] for l in labels]),np.mean([C2[l][i][1] for l in labels]),np.mean([C2[l][i][2] for l in labels])])
        C2_std.append([np.std([C2[l][i][0] for l in labels]),np.std([C2[l][i][1] for l in labels]),np.std([C2[l][i][2] for l in labels])])
    x,y,y_err = get_data_for_plot(C2_means,C2_std,0)
    ax1.errorbar(x,y,yerr=y_err,elinewidth=1,linewidth=3,marker='d',linestyle='-',color=COLORS['c2'],alpha=0.8,label='DAG $c_2$')
    x,y,y_err = get_data_for_plot(C2_means,C2_std,1)
    ax2.errorbar(x,y,yerr=y_err,elinewidth=1,linewidth=3,marker='d',linestyle='-',color=COLORS['c2'],alpha=0.8,label='DAG $c_2$')

    if len(labels)==1:
        ## add horizontal line for number of nodes and edges.
        ax1.plot([0,PL_x_range],[NUM_NODES[labels[0]],NUM_NODES[labels[0]]],'--k',label=labels[0]+' GT')
        ax2.plot([0,PL_x_range],[NUM_EDGES[labels[0]],NUM_EDGES[labels[0]]],'--k',label=labels[0]+' GT')

    # https://matplotlib.org/2.0.2/examples/statistics/errorbar_limits.html
    # ax.errorbar(x, y, xerr=xerr, yerr=yerr, linestyle=ls)

    ax1.legend()
    if len(labels) == 1:
        ax1.set_title('Number of Nodes')
    else:
        ax1.set_title('Avg. Number of Nodes')
    ax1.set_xlabel('Iteration $k$')
    ax1.set_ylabel('# Nodes')
    ax2.legend()
    if len(labels) == 1:
        ax2.set_title('Number of Edges')
    else:
        ax2.set_title('Avg. Number of Edges')
    ax2.set_xlabel('Iteration $k$')
    ax2.set_ylabel('# Edges')

    plt.tight_layout()
    plt.savefig('%s_k%d.png' % ('-'.join(sorted(labels)),k))
    print('saved to %s_k%d.png' % ('-'.join(sorted(labels)),k))
    plt.savefig('%s_k%d.pdf' % ('-'.join(sorted(labels)),k))
    print('saved to %s_k%d.pdf' % ('-'.join(sorted(labels)),k))

    return

def get_data_for_plot(means,stds,index):
    x = range(0,len(means),int(len(means)/20))
    print('x items:',len(x),x)
    y = [means[i][index] for i in x]
    y_err = [stds[i][index] for i in x]
    return x,y,y_err

def get_DAG_output(label,total_k,c):
    DAG = []
    DAG_G = nx.DiGraph()
    G0_file = '../../data/prepare-G0/pathlinker/%s-G0.txt' % (label)
    DAG_file = '../../output/pathlinker-stitched/%s_%s_k%d.txt' % (label,c,total_k)
    print('  ',G0_file)
    print('  ',DAG_file)

    with open(G0_file) as fin:
        for line in fin:
            row = line.strip().split()
            DAG_G.add_edge(row[0],row[1])
    DAG.append(get_stats(DAG_G)) #G0

    with open(DAG_file) as fin:
        for line in fin:
            if line[0] == '#':
                continue
            path = line.strip().split()[2].split('|')
            nx.add_path(DAG_G,path)
            DAG.append(get_stats(DAG_G))
    #print(len(DAG))
    #print(total_k)
    assert total_k+1 == len(DAG)
    return DAG

def get_PL_output(label,k_to_quit):
    PL = []
    PL_G = nx.DiGraph()
    PL_file = glob.glob('../../data/spras-output/%s-pathlinker-params-*/pathway.txt' % (label))[0]
    print('  ',PL_file)
    current_k = 1
    with open(PL_file) as fin:
        for line in fin:
            row = line.strip().split()
            k=int(row[2])
            while k > current_k:
                PL.append(get_stats(PL_G))
                current_k+=1
            if (row[0],row[1]) not in PL_G.edges():
                PL_G.add_edge(row[0],row[1])
            if k > k_to_quit:
                break
    PL.append(get_stats(PL_G))
    assert k == len(PL)
    return PL

def get_GT_output(label):
    GT_file = '../../data/netpath/%s-edges.txt' % (NAMES.get(label,label))
    print(GT_file)
    GT_G = nx.DiGraph()
    c = 0
    with open(GT_file) as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            GT_G.add_edge(row[0],row[1])
            c+=1
    print(c,GT_G.number_of_nodes(),GT_G.number_of_edges())
    return get_stats(GT_G)

def get_stats(G):
    triangle_dict = nx.triangles(G.to_undirected())
    num_triangles = int(sum(triangle_dict.values())/3)
    return [G.number_of_nodes(),G.number_of_edges(),num_triangles]

if __name__ == '__main__':
    labels = sys.argv[1].split(',')
    k = int(sys.argv[2])
    costs = ['c1','c2']
    main(labels,k,costs)
