from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

host = "host.docker.internal:9200"
client = Elasticsearch(host)

class ElasticSearch():
    def __init__(self):
        self.index = ""

    def setIndex(self, indexName):
        self.index = indexName

    def queryIPAddresses(self):
        response = client.search(
            index=self.index,
            body={
            "size":"0",
            "aggs" : {
                "uniq_ipAddresses": {
                "terms": {
                        "field": "ip",
                        "size": 100000
                    },
                }
            }
            }
        )
        uniqueIpAddressesList = [k['key'] for k in response["aggregations"]["uniq_ipAddresses"]["buckets"]]
        return uniqueIpAddressesList

if __name__ == "__main__":
    es = ElasticSearch()
    es.setIndex("kibana_sample_data_logs")
    print(es.queryIPAddresses())