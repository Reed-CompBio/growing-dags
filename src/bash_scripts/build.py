import argparse
import os

## given a k=100, make a G_0 and call for another k=100.

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
NP_PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGF_beta_Receptor','Wnt']

def main():
    args = parse_args()
    out = open(args.bash_file,'w')
    for i in range(len(PATHWAYS)):
        p = PATHWAYS[i]
        np_p = NP_PATHWAYS[i]
        print('PATHWAY',p)
        if not os.path.isdir(args.output_dir):
            os.makedirs(args.output_dir)
        c = args.cost_function
        G0_file = construct_G0(p,args.G0_dir,args.DAG_prefix,args.new_G0_dir,c,args.k)
        if G0_file == None:
            continue
        out.write('echo %s cost %d\n' % (p,c))
        out.write('python3 ../alg/DAG.py ../../data/interactome-weights.txt %s ../../data/netpath/%s-nodes.txt -k 100 -c %d -o %s/%s_c%d_k100.txt > %s/%s_c%d_k100.log &\n' % (G0_file,np_p,c,args.output_dir,p,c,args.output_dir,p,c))
    out.close()
    return

def construct_G0(pathway,original_dir,DAG_prefix,new_dir,c,k):
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    original_path = original_dir+'/'+pathway+'-G0.txt'
    try:
        os.path.exists(original_path)
    except:
        print('File',original_dir+'/'+pathway+'-G0.txt','doesn\'t exist')
        original_path = original_dir+'/'+pathway+'_c%d-G0.txt' % (c)
    DAG_path = DAG_prefix+'/'+pathway +'_c%d_k%d.txt' % (c,k)
    if not os.path.exists(DAG_path):
        print('Skipping',pathway,': this round does not have a DAG.')
        return None
    edges = set()
    with open(original_path) as fin:
        for line in fin:
            edges.add(tuple(line.strip().split()))
    with open(DAG_path) as fin:
        for line in fin:
            if line[0] == '#':
                continue
            path = line.strip().split()[2].split('|')
            for i in range(len(path)-1):
                edges.add(tuple([path[i],path[i+1]]))
    new_path = new_dir+'/'+pathway+'_c%d-G0.txt' % (c)
    out = open(new_path,'w')
    for u,v in edges:
        out.write('%s\t%s\n' % (u,v))
    print('wrote to',new_path)
    return new_path


def parse_args():
    parser = argparse.ArgumentParser(description='Given DAG output, call for another k=100')
    parser.add_argument("G0_dir",help="Directory of G0 files")
    parser.add_argument("DAG_prefix",help="prefix of DAG output directory")
    parser.add_argument("new_G0_dir",help="new G0 directory")
    parser.add_argument("output_dir",help="Output Directory")
    parser.add_argument("bash_file",help="output bash file to write (in bash_scripts/ directory)")
    parser.add_argument('-c',"--cost-function", type=int, choices=[1,2,3], default=2,
    help="Choice of cost function (1, 2, or 3). Default=2.")
    parser.add_argument('-k',type=int,default=100,help="value of k (default is 100)")
    args = parser.parse_args()
    print('ARGUMENTS:',args)
    return args

if __name__ == '__main__':
    main()
