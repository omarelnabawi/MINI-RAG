from LLMEnums import LLmEnum
from providers import OpenAIProvider,CoHereProvider
class LLMProviderFactory:
    def __init__(self,config:dict):
        self.config=config

    def create(self,provider:str):
        if provider==LLmEnum.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temprature=self.config.GENERATION_DEFAULT_TEMPRATURE,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS
            )
        if provider==LLmEnum.COHERE.value:
            return CoHereProvider(
                api_key=self.config.CHOHERE_API_KEY,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temprature=self.config.GENERATION_DEFAULT_TEMPRATURE,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS
            )
        return None