import streamlit as st
from langchain_community.llms import OpenAI
import dotenv
import os

import pprint

import weaviate


dotenv.load_dotenv()

st.title('Document Chatter 📝')

OPENAI_API_KEY = os.getenv("OPENAI_APIKEY")

# Make connection with the Weaviate client, running locally on Docker
client = weaviate.Client(
    url = "http://localhost:8080",
    additional_headers = {
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

# Create the output based on the input text
def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
  return llm(input_text)

# Create the output based on the vector database in Weaviate
def fetch_response_from_weaviate(input_text):
    response = (
        client.query
        .get("DatacenterDocumentsLocal", ["document", "page", "content"])
        .with_near_text({"concepts": [input_text]})
        # This is the system prompt
        # If you want different answers, add it here.
        .with_generate(single_prompt="Answer the prompt " + input_text + " and use the following text: {content}. \
                       Always give the reference as well, using document: '{document}' and pagenumber: '{page}'. \
                       Keep it short and simple, format with lists and newlines.")
        .with_limit(1)
        .do()
    )
    pprint.pprint(response)


    answer = response["data"]["Get"]["DatacenterDocumentsLocal"][0]['_additional']['generate']['singleResult']
    print('Result found!', answer)
    return answer


# Create the streamlit form
with st.form('my_form'):
    text = st.text_area('Enter text:', 'What does the EU say about data center monitoring?')
    choice = st.radio('Select model:', ['GPT', 'RAG'])
    run = st.form_submit_button('Run model')
    if run:
        if choice == 'GPT':
            print('Processing regular OpenAI call...')
            result = generate_response(text)
        elif choice == 'RAG':
            print('Processing RAG call in Weaviate...')
            result = fetch_response_from_weaviate(text)
        st.info(result)
