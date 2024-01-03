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

# First run docker-compose up -d
client = weaviate.Client(
    url="http://localhost:8080",
    additional_headers = {
        "X-OpenAI-Api-Key": OPENAI_API_KEY  
    })

client.schema.delete_all()

# Create class
class_obj = {
    "class": "DatacenterDocumentsLocal",
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
                class_name="DatacenterDocumentsLocal"
            )
