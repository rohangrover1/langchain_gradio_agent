import os
import sys
from dotenv import load_dotenv, find_dotenv
import gradio as gr
from agents import agents
import logging
from agents import match_res_n_model, generate_images, generate_image_v2
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug

llm_model = "dall-e-3"
agentObj = agents(llm_model=llm_model)

def llm_chain_check():
    try:
        from dotenv import load_dotenv, find_dotenv
        _ = load_dotenv(find_dotenv()) # read local .env file
        api_key_str = os.environ['OPENAI_API_KEY']

        set_debug(True)

        llmObj = OpenAI(    
                temperature=0.7,
                model="gpt-3.5-turbo-instruct",
                max_tokens=256
        )

        prompt_template = PromptTemplate(
            input_variables=["image_desc"],
            template="Generate a concise prompt with about 100 words to describe a realistic image, NOT cartoonish, based on the following text: {image_desc}",
        )

        output_parser = StrOutputParser()

        prompt = "elephant riding bike on the moon"
        
        chain = prompt_template | llmObj | output_parser
        llm_respone = chain.invoke(prompt)
        print(llm_respone)
        image_url = DallEAPIWrapper().run(prompt)
        print(image_url)

        # # invoke step by step
        # prompt_response = prompt_template.invoke({"image_desc":prompt})
        # llm_response = llmObj.invoke(prompt_response)
        # print(llm_response)
        # out_response = output_parser.invoke(llm_response)
        # print(out_response)


    except Exception as e:
        logging.error('file:{} line:{} type:{}, message:{}'.format(
                    os.path.basename(__file__), sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))



if __name__ == "__main__":
    try:
        
        llm_chain_check()

        '''
        # setup the gradio chatbot
        with gr.Blocks() as demo:
            gr.Markdown("## DALL-E Image Creation")
            with gr.Row():
                openai_api_key = gr.Textbox(label="OpenAI Key", type="password", value="", placeholder="Enter your OpenAI API key...")
                output_file_path = gr.Textbox(label="Save Log File Path (optional)", placeholder="Enter the file path to save the log file...", type="text")

            with gr.Row():
                prompt = gr.Textbox(label="Prompt", placeholder="Enter your prompt here...")

            generate_button = gr.Button("Generate")
            
            with gr.Row():
                result_text = gr.Textbox(label="Response output:", lines=10, interactive=False)
                images_output = gr.Image(label="Generated Image")

            # if the model changes to "dall-e-3", we need to change the resolution and n
            generate_button.click(
                generate_image_v2,
                inputs=[openai_api_key, output_file_path, prompt],
                outputs=[result_text, images_output]
            )
        
            # with gr.Row():
            #     inputs_x=gr.Textbox(label="image description"),
            #     outputs_x=gr.Image(label="DALL-E Image"),
            # btn2 = gr.Button("Run")
            
            # btn2.click(fn=agentObj.generate_image, inputs=inputs_x[0], outputs=outputs_x[0])

        demo.launch(share=True)
        '''

        # # Gradio interface components
        # with gr.Blocks() as demo:
        #     gr.Markdown("## DALL-E Image Creation")
        #     with gr.Row():
        #         openai_api_key = gr.Textbox(label="OpenAI Key", type="password", value=key, placeholder="Enter your OpenAI API key...")
        #         output_file_path = gr.Textbox(label="Save Log File Path (optional)", placeholder="Enter the file path to save the log file...", type="text")
        #     with gr.Row():
        #         prompt = gr.Textbox(label="Prompt", placeholder="Enter your prompt here...")
        #         n = gr.Slider(minimum=1, maximum=10, step=1, label="Images Requested", value=1)
        #         model = gr.Radio(choices=["dall-e-2", "dall-e-3"], label="Model", value="dall-e-2")
        #         resolution = gr.Radio(choices=["256x256", "512x512", "1024x1024"], label="Image Resolution", value="256x256")
        #     with gr.Row():
        #         quality = gr.Radio(choices=["standard", "hd"], label="Quality", value="standard")
        #         style = gr.Radio(choices=["natural", "vivid"], label="Style", value="natural")
                
        #     generate_button = gr.Button("Generate")
            
        #     with gr.Row():
        #         result_text = gr.Textbox(label="Response output:", lines=10, interactive=False)
        #         images_output = gr.Gallery(label="Generated Images")

        #     # if the model changes to "dall-e-3", we need to change the resolution and n
        #     model.change(match_res_n_model, [model,resolution,n],[resolution,n])
        #     generate_button.click(
        #         generate_images,
        #         inputs=[openai_api_key, output_file_path, prompt, n, resolution, model, style, quality],
        #         outputs=[result_text, images_output]
        #     )
        # demo.launch(share=True)

    except Exception as e:
            logging.error('file:{} line:{} type:{}, message:{}'.format(
                     os.path.basename(__file__), sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))


