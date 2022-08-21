import matplotlib.pyplot as plt

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']

FILE_PREFIXES = {'../../output/pathlinker-G0/%s_c1_k100-prsubsample-%d-50x':'DAG c1',
    '../../output/pathlinker-G0/%s_c2_k100-prsubsample-%d-50x':'DAG c2',
    '../../output/pathlinker/%s-pathlinker-prsubsample-%d-50x':'PL 100',
    '../../output/pathlinker/%s-pathlinker-k1000-prsubsample-%d-50x':'PL 1000'
    }

COLORS = ['#6AB1E2','#376A1D','#DD8C54','#DD8C54']
SHAPES = ['o','d','s','+']
ALPHAS = [1,1,1,0.3]
LWs = [3,3,3,3]
MSs = [8,5,0,0]

def make_fig(k):
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


    fig, axes = plt.subplots(nrows=1, ncols=len(PATHWAYS), figsize=(14,3),sharex=True,sharey=True)
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
        ax.legend()

    plt.tight_layout()
    plt.savefig('precrec-nodes-subsample-%d.png' % (k))
    print('wrote to precrec-nodes-subsample-%d.png' % (k))

    fig, axes = plt.subplots(nrows=1, ncols=len(PATHWAYS), figsize=(15,2),sharex=True,sharey=True)
    for i in range(len(PATHWAYS)):
        pathway = PATHWAYS[i]
        ax = axes[i]
        c = 0
        for name in PRs[pathway]:
            #ax.plot(PRs[pathway][name]['edges']['rec'][0],PRs[pathway][name]['edges']['prec'][0],'o%s' % COLORS[c],ms=MSs[c],label='_nolegend')
            ax.plot(PRs[pathway][name]['edges']['rec'],PRs[pathway][name]['edges']['prec'],color=COLORS[c],alpha=ALPHAS[c],lw=LWs[c],label=name)
            c+=1
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_title(pathway+' Edges')
        ax.legend(loc=4)

    plt.tight_layout()
    plt.savefig('precrec-edges-subsample-%d.png' % (k))
    print('wrote to precrec-edges-subsample-%d.png' % (k))

for i in range(10):
    print('RUNNING ITERATION',i)
    make_fig(i)