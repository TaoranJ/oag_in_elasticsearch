# OAG in Elasticsearch

Want to explore the Microsoft Academic Graph (MAG) and Aminer in a search engine? Use these scripts to put MAG and Aminer dataset in the Elasticsearch!

## Requirement

```bash
pip install elasticsearch tqdm 
```

## Datasets

**OAG** can be downloaded from [here](https://www.openacademic.ai/oag/). **Open Academic Graph (OAG)** unifies two billion-scale academic graphs: **Microsoft Academic Graph (MAG)** and **AMiner**.

### MAG V1

In total, 167 files named in pattern  `mag_papers_[0-166].txt` are included in `MAG V1` dataset. Running the script below to upload the dataset to Elasticsearch. The index name is set up by `--index` option and is `mag_v1` by default. The script was tested on `Elasitcsearch >= 7.4` using English only publications in `MAG V1`.

```bash
python index_mag_v1.py --inputs [path/mag_papers*.txt]
```

### Aminer V1

In total, 155 files named in pattern  `aminer_papers_[0-154].txt` are included in `Aminer V1` dataset. Running the script below to upload the dataset to Elasticsearch. The index name is set up by `--index` option and is `aminer_v1` by default. The script was tested on `Elasitcsearch >= 7.4` and publications which have both title and abstract.

```bash
python index_aminer_v1.py --inputs [path/aminer_papers*.txt]
```
