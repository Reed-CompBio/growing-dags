import sys
import matplotlib.pyplot as plt
import argparse
import os
import random
from sklearn.metrics import auc
from numpy import mean,std

random.seed(123456)

interactome_nodes,interactome_edges = (None,None)

def main():
	args = parseargs()
	print('Processing:',args.pred_file)

	process(args.name,args.pred_file,args.ground_truth_file,args.interactome_file,args.x,args.n,args.k,args.G0_file,args.pathlinker)

def process(name,pred_file,ground_truth_file,interactome_file,x,n,k,G0_file,pathlinker):
	pos_nodes,pos_edges = get_nodes_edges(ground_truth_file)
	print('%d positive nodes and %d positive edges' % (len(pos_nodes),len(pos_edges)))

	# check subsampled negative files; generate them if they don't yet exist.
	check_negs(pos_nodes,pos_edges,ground_truth_file,interactome_file,x,n)

	if pathlinker:
		g0_nodes,g0_edges = (None,None)
	else:
		g0_nodes,g0_edges = get_nodes_edges(G0_file)

	pred_nodes,pred_edges = get_predictions(pred_file,g0_nodes,g0_edges,k,pathlinker=pathlinker)
	print('%d predicted nodes and %d predicted edges (including G0)' % (len(pred_nodes),len(pred_edges)))

	node_aucs = []
	edge_aucs = []
	for i in range(n):
		subsample_node_file = ground_truth_file[:-10]+'/subsampled_negatives/%d_%dx-nodes.txt' % (i,x)
		neg_nodes = get_single_col(subsample_node_file)

		subsample_edge_file = ground_truth_file[:-10]+'/subsampled_negatives/%d_%dx-edges.txt' % (i,x)
		ignore,neg_edges = get_nodes_edges(subsample_edge_file)

		node_aucs.append(pr(pred_nodes,pos_nodes,neg_nodes,name+'subsample-%d-%dx-nodes.txt' % (i,x)))
		edge_aucs.append(pr(pred_edges,pos_edges,neg_edges,name+'subsample-%d-%dx-edges.txt' % (i,x)))

	print('NODE AUC: %f +- %f' % (mean(node_aucs),std(node_aucs)))
	print('EDGE AUC: %f +- %f' % (mean(edge_aucs),std(edge_aucs)))
	return node_aucs,edge_aucs

def parseargs():
	parser = argparse.ArgumentParser(description='precrec')
	parser.add_argument("pred_file",help="output file from DAG.py or Pathlinker")
	parser.add_argument("G0_file",help="Initial DAG (G_0) or 'none' if running pathlinker")
	parser.add_argument("ground_truth_file",help="ground truth file (e.g., NP Pathway)")
	parser.add_argument("interactome_file",help='interactome file to subsample negatives')
	parser.add_argument("name",help="output prefix.")
	parser.add_argument('-p','--pathlinker',action='store_true',help='Compute PR for PathLinker output (default=False).')
	parser.add_argument('-k',type=int,default=1000,help='stop after processing k (default=1000)')
	parser.add_argument('-x',type=int,default=50,help='subsample x times the number of positives (default: 50).')
	parser.add_argument('-n',type=int,default=10,help='number of iterations to sample (default: 10).')
	return parser.parse_args()

def get_single_col(infile):
	nodes = set()
	with open(infile) as fin:
		for line in fin:
			if line[0] == '#':
				continue
			nodes.add(line.strip().split()[0])
	return nodes

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

def pr(pred,pos,neg,outfile):
	out = open(outfile,'w')
	out.write('#prec\trec\t|pred|\t|pos|\t|neg|\tTP\tFP\n')
	x = []
	y = []
	TP = 0
	FP = 0
	prev_k = None
	for item,k in sorted(pred,key = lambda x: x[1]):
		if prev_k == None:
			prev_k = k # set to be 0 or 1, depending on starting count of file.

		if k != prev_k and TP+FP > 0: # write PR, including ties of k.
			# If we've ignored everything, continue until we have at least one TP or FP.
			out.write('%f\t%f\t%d\t%d\t%d\t%d\t%d\n'% (TP/(TP+FP),TP/len(pos),TP+FP,len(pos),len(neg),TP,FP))
			prev_k = k
			x.append(TP/len(pos))
			y.append(TP/(TP+FP))

		if item in pos:
			TP+=1
		elif item in neg:
			FP+=1

	# write final pr
	out.write('%f\t%f\t%d\t%d\t%d\t%d\t%d\n'% (TP/len(pred),TP/len(pos),TP+FP,len(pos),len(neg),TP,FP))
	out.close()
	print('Wrote to %s' % (outfile))
	return auc(x,y)

def check_negs(pos_nodes,pos_edges,ground_truth_file,interactome_file,x,n):
	global interactome_nodes,interactome_edges

	outdir = ground_truth_file[:-10]+'/subsampled_negatives/'
	if not os.path.isdir(outdir):
		print('Making outdirectory',outdir)
		os.makedirs(outdir)

	for i in range(n):
		subsample_node_file = '%d_%dx-nodes.txt' % (i,x)
		subsample_edge_file = '%d_%dx-edges.txt' % (i,x)
		if not os.path.isfile(outdir+subsample_node_file):
			print('WARNING: %s does not exist. Generating it...'  %(subsample_node_file))
			if interactome_nodes == None:
				print("getting interactome nodes and edges...")
				interactome_nodes,interactome_edges = get_nodes_edges(interactome_file)
				print('  %d nodes and %d edges in interactome' % (len(interactome_nodes),len(interactome_edges)))
			cand_neg_nodes = interactome_nodes.difference(pos_nodes)
			num_nodes = min(len(pos_nodes)*x,len(cand_neg_nodes))
			negs = random.sample(list(cand_neg_nodes),num_nodes)
			out= open(outdir+subsample_node_file,'w')
			for n in negs:
				out.write('%s\n' % (n))
			out.close()
			print('Wrote %d negative nodes to %s' %(len(negs),outdir+subsample_node_file))

			cand_neg_edges = interactome_edges.difference(pos_edges)
			num_edges = min(len(pos_edges)*x,len(cand_neg_edges))
			negs = random.sample(list(cand_neg_edges),num_edges)
			out= open(outdir+subsample_edge_file,'w')
			for u,v in negs:
				out.write('%s\t%s\n' % (u,v))
			out.close()
			print('Wrote %d negative edges to %s' %(len(negs),outdir+subsample_edge_file))
	return

def get_pr_at_k(label,k,n,x):
	node_pr_at_ks = {'_c1_':[],'_c2_':[],'-pathlinker-':[]}
	edge_pr_at_ks = {'_c1_':[],'_c2_':[],'-pathlinker-':[]}
	for i in range(n):
		for version in ['_c1_','_c2_','-pathlinker-']:
			if 'pathlinker' not in version:
				nodefile = '../../output/pathlinker-stitched/precrec/%s%sk200-prsubsample-%d-%dx-nodes.txt' % (label,version,i,x)
				edgefile = '../../output/pathlinker-stitched/precrec/%s%sk200-prsubsample-%d-%dx-edges.txt' % (label,version,i,x)
			else:
				nodefile = '../../output/pathlinker/%s%sk200-prsubsample-%d-%dx-nodes.txt' % (label,version,i,x)
				edgefile = '../../output/pathlinker/%s%sk200-prsubsample-%d-%dx-edges.txt' % (label,version,i,x)
			#print(label,nodefile,edgefile)
			with open(nodefile) as fin:
				for line in fin:
					if line[0] == '#':
						continue
					row = line.strip().split()
					if int(row[2]) >= k:
						node_pr_at_ks[version].append(float(row[0]))
						break

			with open(edgefile) as fin:
				for line in fin:
					if line[0] == '#':
						continue
					row = line.strip().split()
					if int(row[2]) >= k:
						edge_pr_at_ks[version].append(float(row[0]))
						break
	print(label,'node lengths:',[len(node_pr_at_ks[x]) for x in ['_c1_','_c2_','-pathlinker-']])
	print(label,'edge lengths:',[len(edge_pr_at_ks[x]) for x in ['_c1_','_c2_','-pathlinker-']])
	return node_pr_at_ks,edge_pr_at_ks
if __name__ == "__main__":
	main()
