# Introduction

Welcome to the Document Searcher. Idea is simple: Ask a question and get the answer from the documents.
It is a Vector Database which is made based on Weaviate. Weaviate is a Vector Database which is based on Graph Database.

## How to use

1. Clone the repository
2. Install the requirements
3. Run the server on docker
4. Run the client using streamlit

### Clone the repository

```bash
git clone
```

### Install the requirements

```bash
pip install -r requirements.txt
```


### Install Docker from the website
To run the code you will need to use Docker. You can download it from the website.

Install link: https://www.docker.com/products/docker-desktop/


### Run the server on docker
This will run the Vector Database on the server.

```bash
docker compose up -d
```

### Create an API key from OpenAI
From OpenAI we will use two things: The word embeddings and the question answering model.
To use this we will need to create an API key from the website.
The costs are not high, but you will need to buy some credits.

Go to the website and create an API key.
Link = https://platform.openai.com/api-keys

### Create .env file
Create a new file called .env in the root directory and add the following line to it.
Add the API key to the file.

```
# .env file
OPENAI_APIKEY="sk-..."

```

### Push the data to the server
This script will read all the pdf files from the data folder and push it to the server.
To add more data to the server, you can add more pdf files to the data folder and run the script again.
Data will not be used to be trained on, but you will need to use the API of OpenAI to get the answers of the model.
If you are not sure if your data can leave your computer, first consult with your company's policy.

```bash
python add_data_to_server.py
```

### Run the client using streamlit
This will start the streamlit server and you can access the website on the browser.
There are two options:
* Get an answer by vanilla ChatGPT, there will not be any knowledge about the documents.
* Get an answer using RAG, the answer will be based on the documents.

```bash
streamlit run application_frontend.py
```
