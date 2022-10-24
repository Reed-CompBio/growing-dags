import argparse
import os
import sys

## given a k=100, make a G_0 and call for another k=100.

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
#NP_PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGF_beta_Receptor','Wnt']

def main():
    args = parse_args()
    if not os.path.isdir(args.new_output_dir):
        print('Making',args.new_output_dir)
        os.makedirs(args.new_output_dir)

    for i in range(len(PATHWAYS)):
        p = PATHWAYS[i]
        print('PATHWAY',p)

        for cost in ['c1','c2']:
            print('  cost',cost)
            f1 = '%s/%s_%s_k%d.txt' % (args.first_output_dir,p,cost,args.k1)
            f2 = '%s/%s_%s_k%d.txt' % (args.second_output_dir,p,cost,args.k2)
            if not os.path.exists(f2):
                print('   skipping...')
                continue
            f_out = '%s/%s_%s_k%d.txt' % (args.new_output_dir,p,cost,args.k1+args.k2)
            print('\tf1: %s\n\tf2: %s\n\tout: %s' % (f1,f2,f_out))

            out = open(f_out,'w')
            out.write('#j\tscore of cost function\tpath\n')
            j = 1
            for f in [f1,f2]:
                with open(f) as fin:
                    for line in fin:
                        if line[0] == '#':
                            continue
                        row = line.strip().split()
                        out.write('%d\t%s\t%s\n' % (j,row[1],row[2]))
                        j+=1
            print('\tfinal j:',j-1)
            out.close()
    return

def parse_args():
    parser = argparse.ArgumentParser(description='Given two directories of k=100 and k=200, stitch together to final output files.')
    parser.add_argument("first_output_dir",help="First Output Directory")
    parser.add_argument("second_output_dir",help="Second Directory")
    parser.add_argument("new_output_dir",help="New Directory")
    parser.add_argument("-k1",type=int,default=100)
    parser.add_argument("-k2",type=int,default=100)
    args = parser.parse_args()
    print('ARGUMENTS:',args)
    return args

if __name__ == '__main__':
    main()
