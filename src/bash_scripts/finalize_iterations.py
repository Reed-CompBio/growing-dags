import sys
import glob

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
NAMES = {'TGFbetaReceptor':'TGF_beta_Receptor'}
NUM_NODES = {'BCR':137,'EGFR1':231,'IL1':43,'TCR':154,'TGFbetaReceptor':209,'Wnt':106}
NUM_EDGES = {'BCR':456,'EGFR1':1456,'IL1':178,'TCR':504,'TGFbetaReceptor':863,'Wnt':428}

# '../../output/pathlinker-stitched_round3/%s_%s_k%d.txt'
DAG_FILES = {'BCR c1':'../../output/pathlinker-stitched_round6/BCR_c1_k1000.txt',
    'BCR c2':'../../output/pathlinker-stitched_round3/BCR_c2_k300.txt',
    'EGFR1 c1':'../../output/pathlinker-stitched_round6/EGFR1_c1_k1000.txt',
    'EGFR1 c2':'../../output/pathlinker-stitched_round6/EGFR1_c2_k1000.txt',
    'IL1 c1':'../../output/pathlinker-stitched/IL1_c1_k200.txt',
    'IL1 c2':'../../output/pathlinker-stitched/IL1_c2_k200.txt',
    'TCR c1':'../../output/pathlinker-stitched_round6/TCR_c1_k1000.txt',
    'TCR c2':'../../output/pathlinker-stitched_round3/TCR_c2_k300.txt',
    'Wnt c1':'../../output/pathlinker-stitched_round4/Wnt_c1_k400.txt',
    'Wnt c2':'../../output/pathlinker-stitched_round3/Wnt_c2_k300.txt',
    'TGFbetaReceptor c1':'../../output/pathlinker-stitched_round6/TGFbetaReceptor_c1_k1000.txt',
    'TGFbetaReceptor c2':'../../output/pathlinker-stitched_round5/TGFbetaReceptor_c2_k600.txt'}

FINAL_OUTDIR = '../../output/pathlinker-final/'

def main():
    print('Pathway Cost NodeK EdgeK')
    for p in PATHWAYS:
        process_PL(p)
        process_DAGs(p)

    print('DONE')

def process_DAGs(p):
    for cost in ['c1','c2']:
        found_node_k = -1
        found_edge_k = -1
        edges = set()
        nodes = set()
        edge_out = open('%s/%s_%s_edges.txt' % (FINAL_OUTDIR,p,cost),'w')
        node_out = open('%s/%s_%s_nodes.txt' % (FINAL_OUTDIR,p,cost),'w')
        with open(DAG_FILES['%s %s' % (p,cost)]) as fin:
            for line in fin:
                if line[0] == '#':
                    continue
                row = line.strip().split()
                k = int(row[0])
                path = row[2].split('|')
                if found_node_k == -1:
                    for i in range(len(path)):
                        nodes.add(path[i])
                    node_out.write(line)
                    if len(nodes) >= NUM_NODES[p]:
                        found_node_k = k
                if found_edge_k == -1:
                    for i in range(len(path)):
                        if i != len(path)-1:
                            edges.add((path[i],path[i+1]))
                    edge_out.write(line)
                    if len(edges) >= NUM_EDGES[p]:
                        found_edge_k = k

                # if we've found both k-values for this cost, break.
                if found_node_k > -1 and found_edge_k > -1:
                    break
        node_out.close()
        edge_out.close()
        if found_node_k == -1:
            found_node_k = 1000
        if found_edge_k == -1:
            found_edge_k = 1000
        print('%s\t%s & %d (%d) & %d (%d)' % (p,cost,len(nodes),found_node_k,len(edges),found_edge_k))
        #sys.exit()
    return

def process_PL(p):
    ## DO THE SAME WITH PATHLINKER
    PL_file = glob.glob('../../data/spras-output/%s-pathlinker-params-*/pathway.txt' % (p))[0]
    #print('  ',PL_file)
    found_node_k = -1
    found_edge_k = -1
    edges = set()
    nodes = set()
    edge_out = open('%s/%s_%s_edges.txt' % (FINAL_OUTDIR,p,'PL'),'w')
    node_out = open('%s/%s_%s_nodes.txt' % (FINAL_OUTDIR,p,'PL'),'w')
    with open(PL_file) as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            k=int(row[2])
            path = row[2].split('|')
            if found_node_k == -1:
                nodes.add(row[0])
                nodes.add(row[1])
                node_out.write(line)
                if len(nodes) >= NUM_NODES[p]:
                    found_node_k = k
            if found_edge_k == -1:
                edges.add((row[0],row[1]))
                edge_out.write(line)
                if len(edges) >= NUM_EDGES[p]:
                    found_edge_k = k

            # if we've found both k-values for this cost, break.
            if found_node_k > -1 and found_edge_k > -1:
                break
    node_out.close()
    edge_out.close()
    if found_node_k == -1:
        found_node_k = 1000
    if found_edge_k == -1:
        found_edge_k = 1000

    print('%s\t%s & %d (%d) & %d (%d)' % (p,'PL',len(nodes),found_node_k,len(edges),found_edge_k))
    return

if __name__ == '__main__':
    main()
