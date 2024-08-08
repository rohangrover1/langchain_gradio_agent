import os
import sys
from langchain.agents import initialize_agent, load_tools
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import logging
import openai
import gradio as gr
import datetime

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
            print(self.llmObj)
            print(self.llmObj.model_name)

            
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


def match_res_n_model(model,resolution,n):
    if model == "dall-e-2":
        n = gr.Slider(minimum=1, maximum=10, step=1, label="Images Requested", value=1, interactive=True)
        return gr.Radio(choices=["256x256", "512x512", "1024x1024"], label="Image Resolution", value="256x256") , n
    else:
        n = gr.Number(value=1, maximum=1, minimum=1, label="Images Requested")
        return gr.Radio(choices=[ "1024x1024"], label="Image Resolution", value="1024x1024"), n
        
        
def generate_images(openai_api_key, output_file_path, prompt, n, resolution, model, style, quality):
    openai.api_key = openai_api_key
    response_text = "Submitting image creation request to OpenAI with the following parameters:\n"
    response_text += f"Prompt: {prompt}\nNumber of images: {n}\nImage resolution: {resolution}\n\n"
    
    try:
        response = openai.images.generate(
            model=model,
            quality=quality,
            style=style,
            prompt=prompt,
            n=n,
            size=resolution
        )
        
        response_text += "Response:\n"
        images_urls = []
        
        for idx in range(0, n):
            url = response.data[idx].url
            images_urls.append(url)
            response_text += f"URL for Image #{idx}: {url}\n"
        
        # Optionally save the response to a file
        if output_file_path != "":   
            with open(output_file_path, "a") as f:
                now = datetime.datetime.now()
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                f.write("-----------------------------\n")
                f.write(date_time + "\n")
                f.write(response_text)
                for url in images_urls:
                    f.write(url + "\n")
        
        return response_text, images_urls
    except openai.OpenAIError as e:
        return f"Error: {str(e)}", []

            
def generate_image_v2(openai_api_key, output_file_path, prompt):
    try:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        llmObj = OpenAI(
                temperature=0.9
            )
        tools = load_tools(["dalle-image-generator"])
        dalle_agent = initialize_agent(tools, llmObj, agent="zero-shot-react-description", verbose=True)
        logging.info("DALL-E agent initialized")

        response_text = dalle_agent.run(prompt)

        print(f"RESPONSE:\n{response_text}")

        image_url = DallEAPIWrapper().run(response_text)

        #  # Optionally save the response to a file
        # if output_file_path != "":   
        #     with open(output_file_path, "a") as f:
        #         now = datetime.datetime.now()
        #         date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        #         f.write("-----------------------------\n")
        #         f.write(date_time + "\n")
        #         f.write(response_text)
        #         f.write(image_url + "\n")
        
        return response_text, image_url
    except Exception as e:
            logging.error('file:{} line:{} type:{}, message:{}'.format(
                     os.path.basename(__file__), sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))
        


