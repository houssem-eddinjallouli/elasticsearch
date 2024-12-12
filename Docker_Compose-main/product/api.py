from retry import retry
import pandas as pd
import elasticsearch
import elasticsearch.helpers

@retry(elasticsearch.ConnectionError, max_delay=300, delay=5)
def indexer():
    es_client = elasticsearch.Elasticsearch(hosts=[{"host": "example_es"}])
    index_name = "example"
    number_of_shards = 1

    # Load CSV data
    df_index = pd.read_csv("/app/data/index_input.csv", na_filter=False)

    # Elasticsearch index settings
    es_params = {
        "index": index_name,
        "body": {
            "settings": {"index": {"number_of_shards": number_of_shards}}
        },
    }

    # Check if the index exists and delete it if needed
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)

    # Create the index
    es_client.indices.create(**es_params)

    # Bulk upload data to Elasticsearch (remove `doc_type`)
    elasticsearch.helpers.bulk(
        es_client,
        df_index.to_dict(orient="records"),
        index=index_name,  # Only specify index, no doc_type
    )

if __name__ == "__main__":
    indexer()
