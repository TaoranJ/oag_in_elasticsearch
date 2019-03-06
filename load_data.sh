# This script is used to create index and insert data.#

index_name='publication'
# create index
curl -X PUT "localhost:9200/$index_name" -H 'Content-Type: application/json' -d '{"settings": {"index" : {"number_of_shards" : 40}}, "mappings": {"doc": {"_field_names": {"enabled": false}, "properties": {"year": {"type": "integer"}, "title": {"type": "text"}, "abstract": {"type": "text"}}}}}'
# update setting
curl -X PUT "localhost:9200/$index_name/_settings" -H 'Content-Type: application/json' -d '{"index" : {"number_of_replicas" : 0, "refresh_interval" : -1}}'
# insert index
find /data/mag/mag.en.index.es/ -type f -print0 | xargs -0 -I {} -n 1 bash -c "curl -o /dev/null -s -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/$index_name/doc/_bulk?pretty' --data-binary @{}"
# reset setting
curl -X PUT "localhost:9200/$index_name/_settings" -H 'Content-Type: application/json' -d '{"index" : {"refresh_interval" : "1s"}}'
