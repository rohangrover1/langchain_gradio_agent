import os
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import ChatPromptTemplate
import gradio as gr
from agents import agents
import logging
from agents import match_res_n_model, generate_images, generate_image_v2
     
# # get the open_ai api key
# _ = load_dotenv(find_dotenv()) # read local .env file
# openai_api_key_str = os.environ['OPENAI_API_KEY']
# print(openai_api_key_str)

llm_model = "dall-e-3"
agentObj = agents(llm_model=llm_model)

if __name__ == "__main__":
    try:

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


