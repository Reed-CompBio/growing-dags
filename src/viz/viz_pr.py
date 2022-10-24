import matplotlib.pyplot as plt

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']

FILE_PREFIXES = {'../../output/pathlinker-stitched/precrec/%s_c1_k200-pr':'DAG c1',
    '../../output/pathlinker-stitched/precrec/%s_c2_k200-pr':'DAG c2',
    '../../output/pathlinker/%s-pathlinker-k200-pr':'PL 200'#,
    #'../../output/pathlinker/%s-pathlinker-k1000-pr':'PL 1000'
    }

COLORS = ['#6AB1E2','#376A1D','#DD8C54','#DD8C54']
SHAPES = ['o','d','s','+']
ALPHAS = [1,1,1,0.3]
LWs = [3,3,3,3]
MSs = [8,5,0,0]


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


fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8,5),sharex=True,sharey=True)
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
    ax.set_title(pathway+' Nodes')
    ax.legend()

plt.tight_layout()
plt.savefig('precrec-nodes.png')
print('wrote to precrec-nodes.png')
plt.savefig('precrec-nodes.pdf')
print('wrote to precrec-nodes.pdf')

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8,5),sharex=True,sharey=True)
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
    ax.set_title(pathway+' Edges')
    ax.legend()

plt.tight_layout()
plt.savefig('precrec-edges.png')
print('wrote to precrec-edges.png')
plt.savefig('precrec-edges.pdf')
print('wrote to precrec-edges.pdf')
