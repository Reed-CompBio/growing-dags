
PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
NAMES = {'TGFbetaReceptor':'TGF_beta_Receptor'}

k =10000
def main():
	make_nodefiles()
	make_unique_nodefiles()
	return

def make_nodefiles():
		for p in PATHWAYS:
			G0_file = '../../data/prepare-G0/pathlinker/%s-G0.txt' % (p)
			g0_nodes,g0_edges = get_nodes_edges(G0_file)

			pathlinker = False

			for c in ['c1','c2']:
				pred_file = '../../output/pathlinker-final/%s_%s_nodes.txt' % (p,c)
				name = '../../output/pathlinker-final/%s_%s_all-nodes.txt' % (p,c)
				print('writing to',name)
				pred_nodes,pred_edges = get_predictions(pred_file,g0_nodes,g0_edges,k,pathlinker)
				out = open(name,'w')
				for n in pred_nodes:
					out.write(n+'\n')
				out.close()

			pathlinker = True
			g0_nodes,g0_edges = (None,None)
			pred_file = '../../output/pathlinker-final/%s_PL_nodes.txt' % (p)
			name = '../../output/pathlinker-final/%s_PL_all-nodes.txt' % (p)
			print('writing to',name)
			pred_nodes,pred_edges = get_predictions(pred_file,g0_nodes,g0_edges,k,pathlinker)
			out = open(name,'w')
			for n in pred_nodes:
				out.write(n+'\n')
			out.close()

def make_unique_nodefiles():
		for p in PATHWAYS:


			c1 = get_nodes('../../output/pathlinker-final/%s_c1_all-nodes.txt' % (p))
			c2 = get_nodes('../../output/pathlinker-final/%s_c2_all-nodes.txt' % (p))
			PL = get_nodes('../../output/pathlinker-final/%s_PL_all-nodes.txt' % (p))


			name = '../../output/pathlinker-final/%s_c1_unique-nodes.txt' % (p)
			print('writing to',name)
			out = open(name,'w')
			for n in c1.difference(c2).difference(PL):
				out.write(n+'\n')
			out.close()

			name = '../../output/pathlinker-final/%s_c2_unique-nodes.txt' % (p)
			print('writing to',name)
			out = open(name,'w')
			for n in c2.difference(c1).difference(PL):
				out.write(n+'\n')
			out.close()

			name = '../../output/pathlinker-final/%s_PL_unique-nodes.txt' % (p)
			print('writing to',name)
			out = open(name,'w')
			for n in PL.difference(c1).difference(c2):
				out.write(n+'\n')
			out.close()

def get_predictions(infile,g0_nodes,g0_edges,max_k,pathlinker=False):
	'''
	Reads a DAG.py output file and returns a set of (node,k) tuples and (edge,k)
	tuples. Includes G0 nodes and edges as k=0.
	'''

	if pathlinker:
		pred_nodes = set()
		encountered_nodes = set()
		pred_edges = set()
		encountered_edges = set()
	else: # add G_0 to preds if processing DAGs
		pred_nodes = set(g0_nodes)
		encountered_nodes = g0_nodes.copy()
		pred_edges = set(g0_edges)
		encountered_edges = g0_edges.copy()

	with open(infile) as fin:
		for line in fin:
			if line[0] == '#':
				continue
			if pathlinker: # treat each edge as a path
				u,v,k = line.strip().split()
				path = '%s|%s' % (u,v)
			else:
				k,score,path =  line.strip().split()
			k = int(k)
			if k > max_k: # quit after seeing k steps
				break
			path = path.split('|')
			for n in path:
				if n not in encountered_nodes:
					encountered_nodes.add(n)
					pred_nodes.add(n)
			for i in range(len(path)-1):
				e = tuple(sorted([path[i],path[i+1]]))
				if e not in encountered_edges:
					encountered_edges.add(e)
					pred_edges.add(e)
	return pred_nodes,pred_edges

def get_nodes_edges(infile):
	'''
	Reads a two-column input file and returns a set of nodes and a set of
	undirected edges (tuples).  Edges are converted to undirected by sorting
	the nodes.
	'''
	edges = set()
	nodes = set()
	with open(infile) as fin:
		for line in fin:
			if line[0] == '#':
				continue
			row= line.strip().split()
			edges.add(tuple(sorted([row[0],row[1]])))
			nodes.add(row[0])
			nodes.add(row[1])
	return nodes,edges


def get_nodes(infile):
	nodes = set()
	with open(infile) as fin:
		for line in fin:
			nodes.add(line.strip())
	return nodes

if __name__ == '__main__':
	main()
