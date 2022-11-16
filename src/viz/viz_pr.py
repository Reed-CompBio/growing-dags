import sys
import matplotlib.pyplot as plt

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']

NODE_FILE_PREFIXES = {'../../output/pathlinker-final/precrec/%s_c1_nodes-pr':'DAG $c_1$',
    '../../output/pathlinker-final/precrec/%s_c2_nodes-pr':'DAG $c_2$',
    '../../output/pathlinker-final/precrec/%s_PL_nodes-pr':'PathLinker'#,
    #'../../output/pathlinker/%s-pathlinker-k1000-pr':'PL 1000'
    }

EDGE_FILE_PREFIXES = {'../../output/pathlinker-final/precrec/%s_c1_edges-pr':'DAG $c_1$',
    '../../output/pathlinker-final/precrec/%s_c2_edges-pr':'DAG $c_2$',
    '../../output/pathlinker-final/precrec/%s_PL_edges-pr':'PathLinker'#,
    #'../../output/pathlinker/%s-pathlinker-k1000-pr':'PL 1000'
    }


COLORS = ['#6AB1E2','#376A1D','#DD8C54','#DD8C54']
SHAPES = ['o','d','s','+']
ALPHAS = [1,1,1,0.3]
LWs = [3,3,3,3]
MSs = [8,5,0,0]

def main(nodes_or_edges):
    if nodes_or_edges == 'nodes':
        FILE_PREFIXES = NODE_FILE_PREFIXES
    else:
        FILE_PREFIXES = EDGE_FILE_PREFIXES

    PRs = {}
    for pathway in PATHWAYS:
        PRs[pathway] = {}
        for f in FILE_PREFIXES:
            name = FILE_PREFIXES[f]
            PRs[pathway][name] = {'nodes':{'prec':[],'rec':[]},'edges':{'prec':[],'rec':[]}}

            for mode in ['nodes','edges']:
                fname = f % pathway + '-' + mode + '.txt'
                #print(fname)

                with open(fname) as fin:
                    for line in fin:
                        if line[0] == '#':
                            continue
                        row =line.strip().split()
                        PRs[pathway][name][mode]['prec'].append(float(row[0]))
                        PRs[pathway][name][mode]['rec'].append(float(row[1]))

    if nodes_or_edges == 'nodes':
        #fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8,5),sharex=True,sharey=True)
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,5))
        axes = [j for sub in axes for j in sub]
        for i in range(len(PATHWAYS)):
            pathway = PATHWAYS[i]
            ax = axes[i]
            c = 0
            for name in PRs[pathway]:
                ax.plot(PRs[pathway][name]['nodes']['rec'][0],PRs[pathway][name]['nodes']['prec'][0],'o',color=COLORS[c],ms=MSs[c],label='_nolegend')
                ax.plot(PRs[pathway][name]['nodes']['rec'],PRs[pathway][name]['nodes']['prec'],COLORS[c],alpha=ALPHAS[c],lw=LWs[c],label=name)
                c+=1
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_ylim(0,1.1)
            ax.set_xlim(-.01,0.5)
            ax.set_title(pathway+' Nodes')
            ax.legend(fontsize=8)

        plt.tight_layout()
        plt.savefig('precrec-fixed-nodes.png')
        print('wrote to precrec-fixed-nodes.png')
        plt.savefig('precrec-fixed-nodes.pdf')
        print('wrote to precrec-fixed-nodes.pdf')

    else:
        #fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8,5),sharex=True,sharey=True)
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,5))
        axes = [j for sub in axes for j in sub]
        for i in range(len(PATHWAYS)):
            pathway = PATHWAYS[i]
            ax = axes[i]
            c = 0
            for name in PRs[pathway]:
                ax.plot(PRs[pathway][name]['edges']['rec'][0],PRs[pathway][name]['edges']['prec'][0],'o',color=COLORS[c],ms=MSs[c],label='_nolegend')
                ax.plot(PRs[pathway][name]['edges']['rec'],PRs[pathway][name]['edges']['prec'],COLORS[c],alpha=ALPHAS[c],lw=LWs[c],label=name)
                c+=1
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_ylim(-.05,1.1)
            ax.set_xlim(-.01,0.55)
            ax.set_title(pathway+' Edges')
            ax.legend(fontsize=8)

        plt.tight_layout()
        plt.savefig('precrec-fixed-edges.png')
        print('wrote to precrec-fixed-edges.png')
        plt.savefig('precrec-fixed-edges.pdf')
        print('wrote to precrec-fixed-edges.pdf')

if __name__ == '__main__':
    main(sys.argv[1])
