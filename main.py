from google.cloud import bigquery
import requests
import os

class Config:
    table_id = os.environ.get("table_id")
    url = os.environ.get("url")

def get_data(url: str) -> dict:
    """Get data via REST API call using requests package
    """
    response = requests.get(url)
    return response.json()

def insert_data(event, context):
    """insert data to bigquery
    Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): 
         context (google.cloud.functions.Context): 
    """
    client = bigquery.Client()

    raw = get_data(Config.url)
    record = [(
        raw["time"]["updatedISO"], 
        raw["bpi"]["THB"]["rate_float"], 
        raw["bpi"]["USD"]["rate_float"]
    )]
    
    table = client.get_table(Config.table_id)
    errors = client.insert_rows(table, record)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
