"""
Need to install openai package using below command
pip install openai==1.13.3
"""


# Add Azure OpenAI package
from openai import AzureOpenAI

import json

# Flag to show citations
show_citations = True

# Get configuration settings
azure_oai_endpoint ="https://eygroup-5.openai.azure.com/"
azure_oai_key ="3d70c3d98fe04860acbb9fb625222366"
azure_oai_deployment ="Group5-AIHackathon"
azure_search_endpoint = "https://group5aisearchservice.search.windows.net"
azure_search_key = "ekxVrvDqv7FRDTHWGfpIK3GisZXXWrrYmuHr53qr7KAzSeCcwgvL"
azure_search_index = "group5index"

# Initialize the Azure OpenAI client
client = AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
            api_key=azure_oai_key,
            api_version="2023-09-01-preview")

# Configure your data source
extension_config = dict(dataSources = [
        {
            "type": "AzureCognitiveSearch",
            "parameters": {
                "endpoint":azure_search_endpoint,
                "key": azure_search_key,
                "indexName": azure_search_index,
            }
        }]
    )

# Get the prompt
text = input('\nEnter your query:\n')

# Send request to Azure OpenAI model
print("...Sending the following request to Azure OpenAI endpoint...")
print("Request: " + text + "\n")

response = client.chat.completions.create(
    model = azure_oai_deployment,
    temperature = 0.5,
    max_tokens = 1000,
    messages = [
         {"role": "system", "content": "You are a helpful assistant who navigates through policy documents and provides answers based on user queries."},
         {"role": "user", "content": text}
            ],
            extra_body = extension_config
        )

# Print response
print("Response: " + response.choices[0].message.content + "\n")

#Check for the citations
if (show_citations):
    # Print citations
    print("Citations:")
    citations = response.choices[0].message.context["messages"][0]["content"]
    citation_json = json.loads(citations)
    for c in citation_json["citations"]:
        print("  Title: " + c['title'] + "\n    URL: " + c['url'])

