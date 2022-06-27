import glob

mapped = {'IL7':'IL-7','IL11':'IL-11','OncostatinM':'Oncostatin_M','TGFbetaReceptor':'TGF_beta_Receptor'}
ppi = {}
with open('interactome-weights.txt') as fin:
    for line in fin:
        row = line.strip().split()
        if row[0] not in ppi:
            ppi[row[0]] = {}
        ppi[row[0]][row[1]] = '%s\t%s\t%s\n' % (row[0],row[1],row[2])

with open('netpath/labels.txt') as fin:
    for line in fin:
        label = line.strip()
        print(label)
        miscounted = []
        out = open('netpath/%s/ground-truth.txt' % (label),'w')
        with open('netpath/%s-edges.txt' % (mapped.get(label,label))) as fin:
            for line in fin:
                if line[0] == '#':
                    continue
                row = line.strip().split()
                if row[0] in ppi and row[1] in ppi[row[0]]:
                    out.write(ppi[row[0]][row[1]])
                else:
                    miscounted.append([row[0],row[1]])
        print('  %d missing' % (len(miscounted)))
        print('  ',miscounted)
        out.close()
