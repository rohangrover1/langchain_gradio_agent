import os
import sys
from langchain.agents import initialize_agent, load_tools
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import logging

# create the chatbot class
class agents():
    def __init__(self, llm_model):
          self.open_ai_key_str = None
          self.dalle_agent = None
          self.llm_model = llm_model
          
    def set_open_ai_key(self, key):
         self.open_ai_key_str = key
         os.environ["OPENAI_API_KEY"] = key
         print("open_ai key set")


    def initialize_dalle_agent(self):
        try:
            if self.open_ai_key_str==None:
                return("please add you open_ai key to proceed")
        
            self.llmObj = OpenAI(
                 temperature=0.9
                 )
            
            tools = load_tools(["dalle-image-generator"])
            self.dalle_agent = initialize_agent(tools, self.llmObj, agent="zero-shot-react-description", verbose=True)
            return("DALL-E agent initialized")

        except Exception as e:
                logging.error('file:{} line:{} type:{}, message:{}'.format(
                     os.path.basename(__file__), sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))


    def generate_image(self, input_text):
        try:
            
            if self.open_ai_key_str==None:
                return("please add you open_ai key in the box above")


            response = self.dalle_agent.run(input_text)
            image_url = DallEAPIWrapper().run(response)
            print(image_url)
            return image_url
        except Exception as e:
            logging.error('file:{} line:{} type:{}, message:{}'.format(
                     os.path.basename(__file__), sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))




            
        


