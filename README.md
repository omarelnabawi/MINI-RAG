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

``` 
 thier are a very helpful structure we can use it by writing as an ex: 'fastapi boilarplate github' in google and you will find many boilerplate code for fastapi application. 
``` 
# what you can find in tut_04_video7?
### we want to upload files:
 - in API we will enter the name of folder and upload the file 
 - we will check it is the size and type sutibele
 - and we will return message depend on problem using `Enum`
 - after that we check the name of folder user enter it is it exist? if no we create it if yes we use it 
 - this step is a bit complicated becouse of we can use `aiofiles` in the file directely and and write it in the folder and that is it but we choose to change create unique_name and simplifie the name of file so at the end it apper in this form => `unique_name +'_'+cleaned_filename` 

# what you can find in tut_05_video8
## we waNT TO Process the file and split it into chunks
### I will start from the HIGH LEVEL (Rout) through functions:
- `data.py` : we create rout that use Processcontroller defination to get [ file_content , file_chunks ] `and` if file_chunks isn't None or 0 we success
- `Processcontroller.py` : we inhreate from `Basecontroller` 
  - use `Projectcontroller` to get project_path 
  - we create `get_file_extintion` to get the extintion of the file.
  - we create `get_file_loader` to test the type of the file extinction by `ProcessEnum` and choose the right loader.
  - after we got the type now we create `get_file_content` to extract the data using the loader 
  - now we need to split the file into chunks using `Langchain` and we choose `RecursiveCharacterTextSplitter` and now we have the chunks.