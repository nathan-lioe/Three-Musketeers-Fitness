#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################
import os
from google.cloud import bigquery

# Create API client
client = bigquery.Client()

# Table name
table_name = f"ise-w-genai.CIS4993.Friends"

# Perform query
def run_query(query):
    query_job = client.query(query)
    # Convert to hashable list format, which allows the caching to work
    rows = [dict(row) for row in query_job.result()]
    return rows

rows = run_query(f"SELECT * FROM `{table_name}`")

print("Some data")
print(rows)


