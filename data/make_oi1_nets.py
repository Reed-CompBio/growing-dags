import glob

mapped = {'IL7':'IL-7','IL11':'IL-11','OncostatinM':'Oncostatin_M','TGFbetaReceptor':'TGF_beta_Receptor'}
ppi = {}
with open('interactome-weights.txt') as fin:
    for line in fin:
        row = line.strip().split()
        if row[0] not in ppi:
            ppi[row[0]] = {}
        ppi[row[0]][row[1]] = '%s\t%s\t%s\n' % (row[0],row[1],row[2])

for label in ['BCR','EGFR1','Wnt','TCR','IL1','TGFbetaReceptor']:
    print(label)
    out = open('netpath/%s/oi1.txt' % (label),'w')
    print('spras-output/%s-omicsintegrator1-params-ZDIIJIU/raw-pathway.txt' % (label))
    with open('spras-output/%s-omicsintegrator1-params-ZDIIJIU/raw-pathway.txt' % (label)) as fin:
        for line in fin:
            if line[0] == '#':
                continue
            row = line.strip().split()
            if row[0] in ppi and row[2] in ppi[row[0]]:
                out.write(ppi[row[0]][row[2]])
            if row[2] in ppi and row[0] in ppi[row[2]]:
                out.write(ppi[row[2]][row[0]])
    out.close()
