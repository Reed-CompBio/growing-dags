import matplotlib.pyplot as plt
import sys

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']

NODE_FILE_PREFIXES = {'../../output/pathlinker-final/precrec/%s_c1_nodes-prsubsample-%d-50x':'DAG $c_1$',
    '../../output/pathlinker-final/precrec/%s_c2_nodes-prsubsample-%d-50x':'DAG $c_2$',
    '../../output/pathlinker-final/precrec/%s-pathlinker-nodes-prsubsample-%d-50x':'PathLinker'#,
    #'../../output/pathlinker/%s-pathlinker-k1000-prsubsample-%d-50x':'PL 1000'
    }


EDGE_FILE_PREFIXES = {'../../output/pathlinker-final/precrec/%s_c1_edges-prsubsample-%d-50x':'DAG $c_1$',
    '../../output/pathlinker-final/precrec/%s_c2_edges-prsubsample-%d-50x':'DAG $c_2$',
    '../../output/pathlinker-final/precrec/%s-pathlinker-edges-prsubsample-%d-50x':'PathLinker'#,
    #'../../output/pathlinker/%s-pathlinker-k1000-prsubsample-%d-50x':'PL 1000'
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

    for i in range(10):
        print('RUNNING ITERATION',i)
        make_fig(FILE_PREFIXES,nodes_or_edges,i)

def make_fig(FILE_PREFIXES,nodes_or_edges,k):
    PRs = {}
    for pathway in PATHWAYS:
        PRs[pathway] = {}
        for f in FILE_PREFIXES:
            name = FILE_PREFIXES[f]
            PRs[pathway][name] = {'nodes':{'prec':[],'rec':[]},'edges':{'prec':[],'rec':[]}}

            for mode in ['nodes','edges']:
                fname = f % (pathway,k) + '-' + mode + '.txt'
                #print(fname)

                with open(fname) as fin:
                    for line in fin:
                        if line[0] == '#':
                            continue
                        row =line.strip().split()
                        PRs[pathway][name][mode]['prec'].append(float(row[0]))
                        PRs[pathway][name][mode]['rec'].append(float(row[1]))

    if nodes_or_edges == 'nodes':
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,5),sharex=True,sharey=True)
        axes = [j for sub in axes for j in sub]
        for i in range(len(PATHWAYS)):
            pathway = PATHWAYS[i]
            ax = axes[i]
            c = 0
            for name in PRs[pathway]:
                ax.plot(PRs[pathway][name]['nodes']['rec'][0],PRs[pathway][name]['nodes']['prec'][0],'o',color= COLORS[c],ms=MSs[c],label='_nolegend')
                ax.plot(PRs[pathway][name]['nodes']['rec'],PRs[pathway][name]['nodes']['prec'],COLORS[c],alpha=ALPHAS[c],lw=LWs[c],label=name)
                c+=1
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title(pathway+' Nodes')
            ax.legend(fontsize=8)

        plt.tight_layout()
        plt.savefig('precrec-fixed-nodes-subsample-%d.png' % (k))
        print('wrote to precrec-fixed-nodes-subsample-%d.png' % (k))
        if k==0:
            plt.savefig('precrec-fixed-nodes-subsample-%d.pdf' % (k))
            print('wrote to precrec-fixed-nodes-subsample-%d.pdf' % (k))
    else:
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,5),sharex=True,sharey=True)
        axes = [j for sub in axes for j in sub]
        for i in range(len(PATHWAYS)):
            pathway = PATHWAYS[i]
            ax = axes[i]
            c = 0
            for name in PRs[pathway]:
                ax.plot(PRs[pathway][name]['edges']['rec'][0],PRs[pathway][name]['edges']['prec'][0],'o',color=COLORS[c],ms=MSs[c],label='_nolegend')
                ax.plot(PRs[pathway][name]['edges']['rec'],PRs[pathway][name]['edges']['prec'],color=COLORS[c],alpha=ALPHAS[c],lw=LWs[c],label=name)
                c+=1
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title(pathway+' Edges')
            ax.legend(loc='best')
            ax.legend(fontsize=8)

        plt.tight_layout()
        plt.savefig('precrec-fixed-edges-subsample-%d.png' % (k))
        print('wrote to precrec-fixed-edges-subsample-%d.png' % (k))
        if k==0:
            plt.savefig('precrec-fixed-edges-subsample-%d.pdf' % (k))
            print('wrote to precrec-fixed-edges-subsample-%d.pdf' % (k))

if __name__ == '__main__':
    main(sys.argv[1])
