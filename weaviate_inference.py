import weaviate

import pprint
import json
import dotenv
import os

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_APIKEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = weaviate.Client(
    url = WEAVIATE_URL,  
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),  
    additional_headers = {
        "X-OpenAI-Api-Key": OPENAI_API_KEY  
    }
)


# response = (
#     client.query
#     .get("DatacenterDocuments", ["document", "page", "content"])
#     .with_near_text({"concepts": ["data center, minimum requirements for monitoring"]})
#     .with_limit(2)
#     .do()
# )

# pprint.pprint(response)

response = (
    client.query
    .get("DatacenterDocuments", ["document", "page", "content"])
    .with_near_text({"concepts": ["data center"]})
    .with_generate(single_prompt="Explain {content} as you might to a five-year-old. {page}")
    .with_limit(1)
    .do()
)

pprint.pprint(response)


# answer = response["data"]["Get"]["DatacenterDocuments"][0]['_additional']['generate']['singleResult']
# print('Here is your anwers ', answer)   

# # Split text into sentences
# # Upload to Weaviate
# results = wev.similarity_search(query="MINIMUM REQUIREMENTS FOR MONITORING AND PUBLISHING THE ENERGY PERFORMANCE OF DATA CENTRES", client=client)

# # Query Weaviate
# # results = vector_store.similarity_search("MINIMUM REQUIREMENTS FOR MONITORING AND PUBLISHING THE ENERGY PERFORMANCE OF DATA CENTRES")
# print('I found several results:')
# for r in results:
#     print('On page ', r.metadata['page'], ' I found: ', r.page_content, '\n\n')

