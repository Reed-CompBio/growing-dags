import sys
out = open('enrichment-tables.tex','w')
out.write('\\newcommand{\\expnumber}[2]{{#1}\\mathrm{e}{#2}}\n')
PATHWAYS = ['BCR','EGFR1','IL1','TCR','TGFbetaReceptor','Wnt']
FILES = ['panther/%s-c1-unique.txt','panther/%s-c2-unique.txt','panther/%s-PL-unique.txt']

for p in ['Wnt']:
    for f in FILES:
        f = f%p
        out.write('\n\n% '+p+' '+f+'\n')
        out.write('\\begin{table}[h]\n')
        out.write('\\centering\n')
        out.write('\\begin{tabular}{|lccc|} \\hline\n')
        out.write('\\textbf{Panther Pathway} & \\textbf{$n$} & \\textbf{$k$} & \\textbf{Adj. P-value} \\\\ \\hline \n')

        start = True
        with open(f) as fin:
            for line in fin:
                row = line.strip().split()
                if start and (len(row)==0 or row[0] != 'PANTHER'):
                    continue
                elif row[0] == 'PANTHER':
                    start = False
                    continue
                else:
                    row = line.strip().split('\t')
                    #print(row)
                    if 'Unclassified' in row[0] or row[4] == '-':
                        continue
                    pval = row[7].split('E')
                    if len(row[0]) < 40:
                        out.write('%s & %s & %s & $\expnumber{%.2f}{%s}$\\\\ \\hline \n' % (row[0],row[1],row[2],float(pval[0]),pval[1]))
                    else:
                        split = row[0].split()
                        mid = int(len(split)/2)
                        print(split)
                        print(mid)
                        print('\t',' '.join(split[:mid]))
                        print('\t',' '.join(split[mid:]))
                        out.write('%s & %s & %s & $\expnumber{%.2f}{%s}$\\\\ \n' % (' '.join(split[:mid]),row[1],row[2],float(pval[0]),pval[1]))
                        out.write('~~~~~%s & & &\\\\ \\hline \n' % (' '.join(split[mid:])))
        out.write('\\end{tabular}\n')
        out.write('\\end{table}\n')

out.close()
print('Wrote to enrichment-tables.tex')
