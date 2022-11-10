from matplotlib_venn import venn3
import matplotlib.pyplot as plt
PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
NAMES = {'TGFbetaReceptor':'TGF_beta_Receptor'}

def main():
	fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12,8))
	axes = [j for sub in axes for j in sub]
	i=0
	for p in PATHWAYS:
		DATA = []
		for c in ['c1','c2']:
			name = '../../output/pathlinker-stitched/%s_%s_k200-nodes.txt' % (p,c)
			DATA.append(get_nodes(name))

		name = '../../output/pathlinker/%s-pathlinker-k200-nodes.txt' % (p)
		DATA.append(get_nodes(name))
		ax = axes[i]
		#print(DATA)
		venn3(DATA,('DAG $c1$','DAG $c2$','PathLinker'),ax=axes[i])
		ax.set_title(p,fontsize=18)
		i+=1
	plt.tight_layout()
	plt.savefig('venn.png')
	plt.savefig('venn.pdf')

	return

def get_nodes(infile):
	nodes = set()
	with open(infile) as fin:
		for line in fin:
			nodes.add(line.strip())
	return nodes
if __name__ == '__main__':
	main()
