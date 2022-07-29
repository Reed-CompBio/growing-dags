# NetPath

Edges and nodes files from `/Users/aritz//Research/VT/vt-svn/data/interactions/netpath/pathways/`

`interactome.txt` from `/Users/aritz//Research/VT/vt-svn/data/interactomes/human/2017_01/2017-01-24-human-ppi-weighted.txt`:

```
cut -f 1-3 /Users/aritz//Research/VT/vt-svn/data/interactomes/human/2017_01/2017-01-24-human-ppi-weighted.txt  > ../interactome.txt
```

In netapath/ dir:

```
cat *-edges.txt | grep -v '#' | sort -u | cut -f 1,2 | grep -v '-' > all-np-edges.txt
 cat /Users/aritz//Documents/github/graphlet-tools/Networks/KEGG_expanded/*-expanded-edges.txt | cut -f 1-2 | grep -v - | sort > all-kegg-edges.txt
```

# SPRAS

To build config file & get input files:

```
cd netpath/
python3 generate-node-files.py
cat labels.txt | awk '{print "ln -s /Users/aritz/Documents/github/growing-dags/data/interactome-weights.txt "$1"/interactome.txt"}' | bash
cd ../
```

Generates the input files and the `config_fragment.txt` file to copy the datasets to the config file in SPRAS.  Need to convert tabs to spaces when you've copied the text. This also symlinks the interactome in each directory.

To run SPRAS (from within `spras/` directory).
```
snakemake --cores 1 --configfile config/growing_dags.yaml
```

To clean dirs:
```
snakemake --cores 1 --configfile config/growing_dags.yaml --until clean
```
