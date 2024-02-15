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



### Run the server on docker

```bash
docker-compose up -d
```

### Create an API key from OpenAI

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

```bash
add_data_to_server.py
```

### Run the client using streamlit
This will start the streamlit server and you can access the website on the browser.

```bash
streamlit run application_frontend.py
```


