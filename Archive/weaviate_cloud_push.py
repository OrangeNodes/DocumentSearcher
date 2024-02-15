from langchain.document_loaders import PyPDFLoader
import weaviate

import requests
import pprint
import glob

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

client.schema.delete_all()

# Create class
class_obj = {
    "class": "DatacenterDocuments",
    "vectorizer": "text2vec-openai", 
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}  
    }
}

client.schema.create_class(class_obj)


# Preprocess data

for pdfpath in glob.glob("data/*.pdf"):
    print('Processing ', pdfpath, '...')

    loader = PyPDFLoader(pdfpath)
    pages = loader.load_and_split()

    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:  # Initialize a batch process
        for i, d in enumerate(pages):  # Batch import data
            d = d.dict()
            properties = {
                "document": d["metadata"]["source"],
                "page": str(d["metadata"]["page"]),
                "content": d["page_content"],
            }
            batch.add_data_object(
                data_object=properties,
                class_name="DatacenterDocuments"
            )