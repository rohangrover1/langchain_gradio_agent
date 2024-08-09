import os
import sys
import langchain.chains
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import logging
from langchain.chains import 



def dalle_chain(openai_api_key, output_file_path, prompt):
    try:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        llmObj = OpenAI(
                temperature=0.9,
        )
        
        chain1 = 


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


