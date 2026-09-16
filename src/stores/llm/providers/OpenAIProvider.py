from llm import LLMinterface,OpenAIEnum
from openai import OpenAI
import logging

class OpenAIProvider(LLMinterface):
    def __init__(self,api_key:str,api_url:str=None,
                 default_input_max_characters:int=1000,
                 default_generation_max_output_tokens:int=1000,
                 default_generation_temprature:float=.1):
        self.api_key=api_key
        self.api_url=api_url

        self.default_input_max_characters=default_input_max_characters
        self.default_generation_max_output_tokens=default_generation_max_output_tokens
        self.default_generation_temprature=default_generation_temprature

        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_model_size=None

        self.client=OpenAI(api_key=self.api_key,api_url=self.api_url)

        self.logger=logging.getLogger(__name__)

        #Take from the text the first 1000 character
        def process_text(self,text:str):
             return text[:self.default_input_max_characters].strip()

        #Define the model of generation
        def set_generation_model(self,model_id:str):
            self.generation_model_id=model_id

        
        #Define the model of embedding and the size
        def set_embedding_model(self,model_id:str,embedding_size=int):
            self.embedding_model_id=model_id
            self.embedding_model_size=embedding_size

        #Generate Text
        def generate_text(self,prompt:str,role:str,max_output_tokens:int=None,
                              temperature:float=None,
                              chat_history:list=[]):
            #Validate the client 
            if not self.client:
                self.logger.error("OpenAI client was not set")
                return None
            #Validate the generateion model
            if not self.generation_model_id:
                 self.logger.error("Generation model for OpenAI was not set")
            #set the max_output & tempreture 
            max_output_tokens=max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
            temperature=temperature if temperature else self.default_generation_temprature
            #Update the History of the chat
            chat_history.append(self.construct_prompt(prompt=prompt,
                                                      role=OpenAIEnum.USER.value))
            #Get the response
            response=self.client.chat.completions.create(
                 model=self.generation_model_id,
                 message=chat_history,
                 max_tokens=max_output_tokens,
                 temperature=temperature
            )
            #Validate the reponse
            if not response or not response.choices or len(response.choices)==0 or not response.choices[0].message:
                 self.logger.error("Error while generating text with OpenAI")
                 return None
            return response.choices[0].message["content"]

        
        #Define the Embedding text 
        def embed_text(self,text:str,document_type:str=None):
            #Validate the client
            if not self.client:
                 self.logger.error("OpenAI client was not set")
                 return None
            #Validate the Embedding model
            if not self.embedding_model_id:
                self.logger.error("Embedding model for OpenAI was not set")
                return None 
            #Create Embedding 
            response =self.client.embeddings.create(
                 model=self.embedding_model_id,
                 input=text
            )
            #Validate the Embedding
            if not response or not response.data or len(response.data)==0 or not response.data[0].choice:
                self.logger.error("Error while embedding text with OpenAI")
                return None
            
            return response
        def construct_prompt(self,prompt:str,role:str):
                return{
                     "role":role,
                     "content":self.process_text(prompt)
                }


    

