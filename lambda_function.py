import os
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import boto3
import logging
from chat_gpt_call import access_api
from call_stability import call_stability
import concurrent.futures
import time

def lambda_handler(event, context):
    start_time = time.time()
    #Code is modified from dream studio example found at: https://platform.stability.ai/docs/getting-started/authentication
    return_dict = {"completion": False,
                "url": None,
                "message":None,
                }
    phrase = event['phrase']
    story = event.get('story',{})
     #access chat GPT to progress the story:
    returned_messages, returned_options, returned_iterator, returned_good_flag, returned_end_flag = access_api(prompt=event['phrase'], 
                                                                                                               messages=story.get("returned_messages",None),
                                                                                                               user_response = story.get("user_response", None), 
                                                                                                               good_flag = story.get("returned_good_flag", True), 
                                                                                                               iterator = story.get("returned_iterator",0))
    return_dict['story'] = {"returned_messages":returned_messages, "returned_options":returned_options, "returned_iterator":returned_iterator, "returned_good_flag":returned_good_flag, "returned_end_flag":returned_end_flag}
    access_key=os.environ.get('REACT_APP_accessKeyId')
    secret_key=os.environ.get('REACT_APP_secretAccessKey')
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_key = {executor.submit(call_stability, return_dict['story']['returned_messages'][-1]['content'], key): key for key in returned_options}
            for future in concurrent.futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    response = future.result()
                    if response["url"]:
                        returned_options[key] = response["url"]
                except Exception as e:
                    print(f"Error: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 30:
            time.sleep(30 - elapsed_time)
        return return_dict
    except Exception as e:
        return_dict["message"] = e
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 30:
            time.sleep(30 - elapsed_time)
        return return_dict
