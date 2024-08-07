import os
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import ChatPromptTemplate
import gradio as gr
from agents import agents
import logging

     
# # get the open_ai api key
# _ = load_dotenv(find_dotenv()) # read local .env file
# openai_api_key_str = os.environ['OPENAI_API_KEY']
# print(openai_api_key_str)

llm_model = "dall-e-2"
agentObj = agents(llm_model=llm_model)

if __name__ == "__main__":
    try:
        # setup the gradio chatbot
        with gr.Blocks() as demo:
            with gr.Row():
                with gr.Column(scale=1, variant="compact"):
                    gr.Markdown("Enter you open API key")
                    inp = gr.Textbox(placeholder="open API Key")                
                    btna = gr.Button("Enter")
                btna.click(fn=agentObj.set_open_ai_key, inputs=inp)    


            with gr.Row():
                out_x=gr.Textbox(label="status", scale=1),
            btn1 = gr.Button("Initialize DALL-E Agent", scale=1)    
            btn1.click(fn=agentObj.initialize_dalle_agent, outputs=out_x[0])    

            with gr.Row():
                inputs_x=gr.Textbox(label="image description"),
                outputs_x=gr.Image(label="DALL-E Image"),
            btn2 = gr.Button("Run")
            btn2.click(fn=agentObj.generate_image, inputs=inputs_x[0], outputs=outputs_x[0])

        demo.launch()

    except Exception as e:
            logging.error('file:{} line:{} type:{}, message:{}'.format(
                     os.path.basename(__file__), sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))


