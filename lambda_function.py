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

def lambda_handler(event, context):
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
        for key in returned_options:
            response = call_stability(return_dict['story']['returned_messages'][-1]['content'], key)
            if response["url"]:
                returned_options[key] = response["url"]
        return return_dict
    except Exception as e:
        return_dict["message"] = e
        return return_dict
    