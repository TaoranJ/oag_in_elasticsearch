# OAG in Elasticsearch

Want to explore the Microsoft Academic Graph (MAG) and Aminer in a search engine? Use these scripts to put MAG and Aminer dataset in the Elasticsearch!

## Download OAG

Download **OAG** from [here](https://www.openacademic.ai/oag/). **Open Academic Graph (OAG)** unifies two billion-scale academic graphs: **Microsoft Academic Graph (MAG)** and **AMiner**.


## MAG V1

In total, there are 167 files included in `MAG V1` dataset with name `mag_papers_[0-166].txt`. Each line of each file has the JSON format. The following scrip will load the entire dataset to Elasticsearch. By default, the index name is `mag_v1`. It can be changed by setting `--index [index_name]`.

```bash
python index_mag_v1.py --inputs [path/mag_papers*.txt]
```
