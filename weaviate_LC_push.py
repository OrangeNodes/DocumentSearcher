from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.weaviate import Weaviate

import weaviate

import dotenv
import os

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = weaviate.Client(
    url = WEAVIATE_URL,  
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),  
    additional_headers = {
        "X-OpenAI-Api-Key": OPENAI_API_KEY  
    }
)

# Preprocess data
loader = PyPDFLoader("data/EU_Green_Deal.pdf")
pages = loader.load_and_split()

print('The third page = ', pages[2])
print('==================== \n\n')

embeddings = OpenAIEmbeddings()

# Split text into sentences
# Upload to Weaviate
vector_store = Weaviate.from_documents(pages, embeddings, client=client, by_text=False)

# Query Weaviate
results = vector_store.similarity_search("MINIMUM REQUIREMENTS FOR MONITORING AND PUBLISHING THE ENERGY PERFORMANCE OF DATA CENTRES")
print('I found several results:')
for r in results:
    print('On page ', r.metadata['page'], ' I found: ', r.page_content, '\n\n')

