
import importlib
pr_sub   = importlib.import_module("precrec-subsample")
pr   = importlib.import_module("precrec")
from numpy import mean,std,isnan

PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
NAMES = {'TGFbetaReceptor':'TGF_beta_Receptor'}
DISPLAY_NAMES = {'TGFbetaReceptor':'TGF$\\beta$'}

interactome_file = '../../data/interactome-weights.txt'
x = 50
k = 10000
n = 10

out = open('auc-table.tex','w')

out.write('\n\n% SUBSAMPLED AUCs\n')
out.write('\\begin{table}[h]\n')
out.write('\\centering\n')
out.write('\\begin{tabular}{|l|ccc|} \\hline\n')
out.write('\\textbf{Name} & \\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PathLinker} \\\\ \\hline \n')
for p in PATHWAYS:
    outline1 = DISPLAY_NAMES.get(p,p)+' nodes'
    outline2 = DISPLAY_NAMES.get(p,p)+' edges'
    # python precrec-subsample.py ../../output/pathlinker-final/Wnt_c1_k200.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-edges.txt ../../data/interactome-weights.txt ../../output/pathlinker-final/precrec/Wnt_c1_k200-pr
    # process(args.name,args.pred_file,args.ground_truth_file,args.interactome_file,args.x,args.n,args.k,args.G0_file,args.pathlinker)
    G0_file = '../../data/prepare-G0/pathlinker/%s-G0.txt' % (p)
    ground_truth_file = '../../data/netpath/%s-edges.txt' % (NAMES.get(p,p))

    pathlinker = False
    node_auc_list = []
    edge_auc_list = []
    for c in ['c1','c2']:
        pred_file = '../../output/pathlinker-final/%s_%s_nodes.txt' % (p,c)
        name = '../../output/pathlinker-final/precrec/%s_%s_nodes-pr' % (p,c)
        node_aucs,ignore = pr_sub.process(name,pred_file,ground_truth_file,interactome_file,x,n,k,G0_file,pathlinker)
        node_auc_list.append(node_aucs)

        pred_file = '../../output/pathlinker-final/%s_%s_edges.txt' % (p,c)
        name = '../../output/pathlinker-final/precrec/%s_%s_edges-pr' % (p,c)
        ignore,edge_aucs = pr_sub.process(name,pred_file,ground_truth_file,interactome_file,x,n,k,G0_file,pathlinker)
        edge_auc_list.append(edge_aucs)

    pathlinker = True
    pred_file = '../../output/pathlinker-final/%s_PL_nodes.txt' % (p)
    name = '../../output/pathlinker-final/precrec/%s-pathlinker-nodes-pr' % (p)
    node_aucs,ignore = pr_sub.process(name,pred_file,ground_truth_file,interactome_file,x,n,k,G0_file,pathlinker)
    node_auc_list.append(node_aucs)

    pred_file = '../../output/pathlinker-final/%s_PL_edges.txt' % (p)
    name = '../../output/pathlinker-final/precrec/%s-pathlinker-edges-pr' % (p)
    ignore,edge_aucs = pr_sub.process(name,pred_file,ground_truth_file,interactome_file,x,n,k,G0_file,pathlinker)
    edge_auc_list.append(edge_aucs)

    max_node_auc = max([mean(n) for n in node_auc_list])
    max_edge_auc = max([mean(n) for n in edge_auc_list])
    for i in range(len(node_auc_list)):
        node_aucs = node_auc_list[i]
        if mean(node_aucs) == max_node_auc:
            outline1 += ' & $\\mathbf{%.3f \\pm %.2f}$' % (mean(node_aucs),std(node_aucs))
        else:
            outline1 += ' & $%.3f \\pm %.2f$' % (mean(node_aucs),std(node_aucs))
        edge_aucs = edge_auc_list[i]
        if mean(edge_aucs) == max_edge_auc:
            outline2 += ' & $\\mathbf{%.3f \\pm %.2f}$' % (mean(edge_aucs),std(edge_aucs))
        else:
            outline2 += ' & $%.3f \\pm %.2f$' % (mean(edge_aucs),std(edge_aucs))

    out.write(outline1+'\\\\ \n')
    out.write(outline2+'\\\\ \\hline \n')

out.write('\\end{tabular}\n')
out.write('\\end{table}\n')

out.write('\n\n% SUBSAMPLED PRECISION @25\n')
out.write('\\begin{table}[h]\n')
out.write('\\centering\n')
out.write('\\begin{tabular}{|l|ccc|ccc|} \\hline\n')
out.write('\\textbf{Name} & \\multicolumn{3}{c|}{\\textbf{Node Precision @25}} & \\multicolumn{3}{c|}{\\textbf{Edge Precision @25}} \\\\\n')
out.write(' & \\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PL} &\\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PL} \\\\ \\hline \n')
for p in PATHWAYS:
    outline = DISPLAY_NAMES.get(p,p)

    node_pr_at_ks,edge_pr_at_ks = pr_sub.get_pr_at_k(p,25,n,x)
    node_max = max(mean(x) for x in node_pr_at_ks.values())
    edge_max = max(mean(x) for x in edge_pr_at_ks.values())
    for version in ['_c1_','_c2_','-pathlinker-']:
        if isnan(mean(node_pr_at_ks[version])):
            outline += ' & '
        elif mean(node_pr_at_ks[version]) == node_max:
            outline += ' & $\\mathbf{%.3f \\pm %.2f}$' % (mean(node_pr_at_ks[version]),std(node_pr_at_ks[version]))
        else:
            outline += ' & $%.3f \\pm %.2f$' % (mean(node_pr_at_ks[version]),std(node_pr_at_ks[version]))

    for version in ['_c1_','_c2_','-pathlinker-']:
        if isnan(mean(edge_pr_at_ks[version])):
            outline += ' & '
        elif mean(edge_pr_at_ks[version]) == edge_max:
            outline += ' & $\\mathbf{%.3f \\pm %.2f}$' % (mean(edge_pr_at_ks[version]),std(edge_pr_at_ks[version]))
        else:
            outline += ' & $%.3f \\pm %.2f$' % (mean(edge_pr_at_ks[version]),std(edge_pr_at_ks[version]))
    out.write(outline+'\\\\ \\hline \n')

out.write('\\end{tabular}\n')
out.write('\\end{table}\n')

out.write('\n\n% ORIGINAL AUCs\n')
out.write('\\begin{table}[h]\n')
out.write('\\centering\n')
out.write('\\begin{tabular}{|l|ccc|ccc|} \\hline\n')
out.write('\\textbf{Name} & \\multicolumn{3}{c|}{\\textbf{Node AUC}} & \\multicolumn{3}{c|}{\\textbf{Edge AUC}} \\\\\n')
out.write(' & \\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PL} &\\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PL} \\\\ \\hline \n')
for p in PATHWAYS:
    outline = DISPLAY_NAMES.get(p,p)

    #process(ground_truth_file,G0_file,pred_file,k,pathlinker,name)
    G0_file = '../../data/prepare-G0/pathlinker/%s-G0.txt' % (p)
    ground_truth_file = '../../data/netpath/%s-edges.txt' % (NAMES.get(p,p))

    pathlinker = False
    node_auc_list = []
    edge_auc_list = []
    for c in ['c1','c2']:
        pred_file = '../../output/pathlinker-final/%s_%s_nodes.txt' % (p,c)
        name = '../../output/pathlinker-final/precrec/%s_%s_nodes-pr' % (p,c)
        node_aucs,ignore = pr.process(ground_truth_file,G0_file,pred_file,k,pathlinker,name)
        node_auc_list.append(node_aucs)

        pred_file = '../../output/pathlinker-final/%s_%s_edges.txt' % (p,c)
        name = '../../output/pathlinker-final/precrec/%s_%s_edges-pr' % (p,c)
        ignore,edge_aucs = pr.process(ground_truth_file,G0_file,pred_file,k,pathlinker,name)
        edge_auc_list.append(edge_aucs)

    pathlinker = True
    pred_file = '../../output/pathlinker-final/%s_PL_nodes.txt' % (p)
    name = '../../output/pathlinker-final/precrec/%s-pathlinker-nodes-pr' % (p)
    node_aucs,ignore = pr.process(ground_truth_file,G0_file,pred_file,k,pathlinker,name)
    node_auc_list.append(node_aucs)

    pred_file = '../../output/pathlinker-final/%s_PL_edges.txt' % (p)
    name = '../../output/pathlinker-final/precrec/%s-pathlinker-edges-pr' % (p)
    ignore,edge_aucs = pr.process(ground_truth_file,G0_file,pred_file,k,pathlinker,name)
    edge_auc_list.append(edge_aucs)

    max_node_auc = max(node_auc_list)
    max_edge_auc = max(edge_auc_list)
    for i in range(len(node_auc_list)):
        node_aucs = node_auc_list[i]
        if node_aucs == max_node_auc:
            outline += ' & $\\mathbf{%.3f}$' % (node_aucs)
        else:
            outline += ' & $%.3f$' % (node_aucs)
    for i in range(len(node_auc_list)):
        edge_aucs = edge_auc_list[i]
        if edge_aucs == max_edge_auc:
            outline += ' & $\\mathbf{%.3f}$' % (edge_aucs)
        else:
            outline += ' & $%.3f$' % (edge_aucs)
    out.write(outline+'\\\\ \\hline \n')

out.write('\\end{tabular}\n')
out.write('\\end{table}\n')

out.write('\n\n% PRECISION @50\n')
out.write('\\begin{table}[h]\n')
out.write('\\centering\n')
out.write('\\begin{tabular}{|l|ccc|ccc|} \\hline\n')
out.write('\\textbf{Name} & \\multicolumn{3}{c|}{\\textbf{Node Precision @50}} & \\multicolumn{3}{c|}{\\textbf{Edge Precision @50}} \\\\\n')
out.write(' & \\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PL} &\\textbf{DAG $c_1$} & \\textbf{DAG $c_2$} & \\textbf{PL} \\\\ \\hline \n')
for p in PATHWAYS:
    outline = DISPLAY_NAMES.get(p,p)

    node_pr_at_ks,edge_pr_at_ks = pr.get_pr_at_k(p,50)
    node_max = max(node_pr_at_ks.values())
    edge_max = max(edge_pr_at_ks.values())
    for version in ['_c1_','_c2_','-pathlinker-']:
        if node_pr_at_ks[version] == -1:
            outline += ' & '
        elif node_pr_at_ks[version] == node_max:
            outline += ' & $\\mathbf{%.3f}$' % (node_pr_at_ks[version])
        else:
            outline += ' & $%.3f$' % (node_pr_at_ks[version])

    for version in ['_c1_','_c2_','-pathlinker-']:
        if edge_pr_at_ks[version] == -1:
            outline += ' & '
        elif edge_pr_at_ks[version] == edge_max:
            outline += ' & $\\mathbf{%.3f}$' % (edge_pr_at_ks[version])
        else:
            outline += ' & $%.3f$' % (edge_pr_at_ks[version])
    out.write(outline+'\\\\ \\hline \n')

out.write('\\end{tabular}\n')
out.write('\\end{table}\n')
out.close()
