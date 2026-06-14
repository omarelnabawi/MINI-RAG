# MINI-RAG
let's create RAG System with each other
## Requirments
- Python 3.8 or latter

### Install Python using MiniConda 

1) Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install)
2)Create a new envirnment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the envirnoment:
```bash
$ conda activate mini-rag 
```
### (Optional) Setup you command line interface for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation
### Install the required package
```bash
$ pip install -r requirements.txt
```
### Set up the environment variables

```bash
$ cp .env.example .env
```
set your environment variables in the `.env` file. Like 'OPENAI_API_KEY' for value. 

## Usage
### Run the FastAPI application
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
### What Does it mean?
- `uvicorn main:app` tells Uvicorn to run the FastAPI application defined in the `main.py` file, where `app` is the instance of the FastAPI application.
- `--reload` enables auto-reloading of the server when code changes are detected, which is useful during development.
- `--host 0.0.0.0` makes the server accessible from any IP address.
- `--port 5000` specifies the port on which the server will run.
### Postman Collection
Download the Postman collection from [here](/assets/MINI_RAG%20V%202.0.postman_collection.json) and import it into your Postman application
### Include the base router in your FastAPI application
```bash
$ app.include_router(base.base_router)
```
This line of code is used to include the base router in your FastAPI application. The `base_router` is defined in the `base` module, which is imported at the beginning of the `main.py` file. By including the router, you can access the endpoints defined in the `base_router` when you run your FastAPI application.