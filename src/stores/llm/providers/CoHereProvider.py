from LLMinterface import LLMinterface
from llm import CoHereEnum,DocumentTypeEnum
import logging
import cohere

class CoHereProvider(LLMinterface):

    def __init__(self,api_key:str,
                 default_input_max_characters:int=1000,
                 default_generation_max_output_tokens:int=1000,
                 default_generation_temprature:float=.1):
        
        self.api_key=api_key
        
        self.default_input_max_characters=default_input_max_characters
        self.default_generation_max_output_tokens=default_generation_max_output_tokens
        self.default_generation_temprature=default_generation_temprature
        
        self.generation_model_id=None
        
        self.embedding_model_id=None
        self.embedding_model_size=None

        self.client=cohere.Client(api_key=self.api_key)

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
                                                      role=CoHereEnum.USER.value))
            #Get the response
            response=self.client.chat(
                model=self.generation_model_id,
                chat_history=chat_history,
                message=self.process_text(prompt)
            )
            #Validate the reponse
            if not response or not response.text:
                 self.logger.error("Error while generating text with CoHere")
                 return None
            return response.text

        
        #Define the Embedding text 
        def embed_text(self,text:str,document_type:str=None):
            #Validate the client
            if not self.client:
                 self.logger.error("CoHere client was not set")
                 return None
            #Validate the Embedding model
            if not self.embedding_model_id:
                self.logger.error("Embedding model for CoHere was not set")
                return None 

            input_type=CoHereEnum.DOCUMNET
            if document_type ==DocumentTypeEnum.QUERY:
                 input_type=CoHereEnum.QUERY
            #Create Embedding 
            response =self.client.embed(
                 model=self.embedding_model_id,
                 texts=[self.process_text(text)],
                 input_type=document_type,
                 embedding_types=['float']
            )
            #Validate the Embedding
            if not response or not  response.embeddings or not response.embeddings.float:
                self.logger.error("Error while embedding text with CoHere")
                return None
            
            return response.embeddings.float[0]
        def construct_prompt(self,prompt:str,role:str):
                return{
                     "role":role,
                     "content":self.process_text(prompt)
                }


    
