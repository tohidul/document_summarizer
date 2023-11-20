# Document Summarization
This is a demo project to demonstrate the perfornmace of celery group
tasks.

## Setup
Install the dependencies using the following command
`pip install -r requrements.txt`

See the example_config.py file to setup database
and celery configurations

To run a development server:

Go the document_summarization directory

`export CONFIG_FILE=<path to config file>`

Run the following command in terminal.

`python -m flask --app app run --debug`

## Usage:
Add Documents:

`curl --location 'http://<host>:<port>/add_documents' \
--form 'document_list="<document_path>"' \
--form 'document_list="<document_path>"'`

Run Summarization Task:

`curl --location 'http://<host>:<port>/summarize' \
--form 'number_of_concurrent_task="<number of concurrent task>"'`

Retrieve Document Summaries:

`curl --location 'http://<host>:<port>/get_summary?document_id_list=<document_id>&document_id_list=<document_id>'`