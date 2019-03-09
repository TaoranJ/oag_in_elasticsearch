# MAG in Elasticsearch

Want to explore the Microsoft Academic Graph (MAG) in a search engine? Use these scripts to put MAG dataset in the Elasticsearch!

## Quickstart
### Requirements

```bash
pip install elasticsearch, python-dateutil
```

### Download MAG

Download **OAG** from [here](https://www.openacademic.ai/oag/). **Open Academic Graph (OAG)** unifies two billion-scale academic graphs: **Microsoft Academic Graph (MAG)** and **AMiner**. Currently, there exists two versions of OAG, and these scripts are tested on MAG extracted from **OAG V1**. `166,192,182` papers are included in dataset.

In total, there are 167 files included in MAG dataset with name `mag_papers_[0-166].txt`. Given a specific file, say, `mag_papers_0.txt`, each line of it is in JSON format.


### Insert index in MAG data

```bash
# use multiple cores to index data in parallel
python gen_index.py --cores [cpus_to_use] [output_path] [input_paths]
```

In scrip `gen_index.py`, only the fields `id`, `year`, `title`, `abstract`, `fos` and `keywords` are taken care, though there are many other fileds in the original datafile. See [here](https://www.openacademic.ai/oag/) for details.

After indexing, the file looks like below.
```json
{"index": {"_index": "publication", "_id": "0000002e-c2f2-4e25-9341-60d39130ac7a"}}
{"year": 2015, "title": "system and method for maskless direct write lithography", "abstract": "a system and method for maskless direct write lithography are disclosed. the method includes receiving a plurality of pixels that represent an integrated circuit (ic) layout; identifying a first subset of the pixels that are suitable for a first compression method; and identifying a second subset of the pixels that are suitable for a second compression method. the method further includes compressing the first and second subset using the first and second compression method respectively, resulting in compressed data. the method further includes delivering the compressed data to a maskless direct writer for manufacturing a substrate. in embodiments, the first compression method uses a run-length encoding and the second compression method uses a dictionary-based encoding. due to the hybrid compression method, the compressed data can be decompressed with a data rate expansion ratio sufficient for high-volume ic manufacturing.", "fos": ["electronic engineering", "computer hardware", "engineering", "engineering drawing"], "keywords": []}
```

Next, it's time to load dataset into `Elasticsearch`. By default, `Elasticsearch` supports to insert file which is less than `100MB`. So if you don't want to adjust this value in `Elasticsearch` configuration file, simplly use the 
```bash
mkdir mag.es
cat [mag_dataset]/* > mag.es/mag.total
cd mag.es
split -l 80000 mag.total
rm mag.total
```

### Insert MAG into Elasticsearch

```bash
bash load_data.sh
```
