from abc import ABC,abstractclassmethod

class LLMinterface(ABC):

    @abstractclassmethod
    def set_generation_model(self,model_id:str):
        pass

    @abstractclassmethod
    def set_embedding_model(self,model_id:str,embedding_size=int):
        pass

    @abstractclassmethod
    def generate_text(self,prompt:str,role:str,max_output_tokens:int=None,
                      temperature:float=None,
                      chat_history:list=[]):
        pass

    @abstractclassmethod
    def embed_text(self,text:str,document_type:str=None):
        pass

    @abstractclassmethod
    def construct_prompt(self,prompt:str,role:str):
        pass