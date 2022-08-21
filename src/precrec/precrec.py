import sys
import matplotlib.pyplot as plt
import argparse

def main():
	args = parseargs()
	print(args)

	pos_nodes,pos_edges = get_nodes_edges(args.ground_truth_file)
	print('%d positive nodes and %d positive edges' % (len(pos_nodes),len(pos_edges)))

	if args.pathlinker:
		g0_nodes,g0_edges = (None,None)
	else:
		g0_nodes,g0_edges = get_nodes_edges(args.G0_file)

	pred_nodes,pred_edges = get_predictions(args.pred_file,g0_nodes,g0_edges,args.k,pathlinker=args.pathlinker)
	print('%d predicted nodes and %d predicted edges (including G0)' % (len(pred_nodes),len(pred_edges)))

	pr(pred_nodes,pos_nodes,args.name+'-nodes.txt')
	pr(pred_edges,pos_edges,args.name+'-edges.txt')

	return

def parseargs():
	parser = argparse.ArgumentParser(description='precrec')
	parser.add_argument("pred_file",help="output file from DAG.py or Pathlinker")
	parser.add_argument("G0_file",help="Initial DAG (G_0) or 'none' if running pathlinker")
	parser.add_argument("ground_truth_file",help="ground truth file (e.g., NP Pathway)")
	parser.add_argument("name",help="output prefix.")
	parser.add_argument('-p','--pathlinker',action='store_true',help='Compute PR for PathLinker output (default=False).')
	parser.add_argument('-k',type=int,default=100,help='stop after processing k (default=100)')
	return parser.parse_args()

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
		pred_nodes = set([(n,0) for n in g0_nodes])
		encountered_nodes = g0_nodes.copy()
		pred_edges = set([(e,0) for e in g0_edges])
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
					pred_nodes.add((n,k))
			for i in range(len(path)-1):
				e = tuple(sorted([path[i],path[i+1]]))
				if e not in encountered_edges:
					encountered_edges.add(e)
					pred_edges.add((e,k))
	return pred_nodes,pred_edges

def pr(pred,pos,outfile):
	out = open(outfile,'w')
	out.write('#prec\trec\t|pred|\t|pos|\tTP\tFP\n')

	TP = 0
	FP = 0
	prev_k = None
	for item,k in sorted(pred,key = lambda x: x[1]):
		if prev_k == None:
			prev_k = k # set to be 0 or 1, depending on starting count of file.
			
		if k != prev_k: # write PR, including ties of k.
			out.write('%f\t%f\t%d\t%d\t%d\t%d\n'% (TP/(TP+FP),TP/len(pos),TP+FP,len(pos),TP,FP))
			prev_k = k
		(k,item,item in pos)
		if item in pos:
			TP+=1
		else:
			FP+=1
	# write final pr
	out.write('%f\t%f\t%d\t%d\t%d\t%d\n'% (TP/len(pred),TP/len(pos),TP+FP,len(pos),TP,FP))
	out.close()
	print('Wrote to %s' % (outfile))
	return



if __name__ == "__main__":
	main()
