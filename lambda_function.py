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
import json


log = logging.getLogger(__name__)
log_stream = io.StringIO()    
logging.basicConfig(stream=log_stream, level=logging.INFO)
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
        s3 = boto3.client('s3', aws_access_key_id=access_key,aws_secret_access_key=secret_key)

        dream = os.environ.get('dream')
        bucket = os.environ.get('bucket')

        os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
        os.environ['STABILITY_KEY'] = dream

        stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'], 
            verbose=True, 
            engine="stable-diffusion-v1-5", 
            
        )

        # Set up our initial generation parameters.
        answers = stability_api.generate(
            prompt=phrase,   
            steps=30, 
            cfg_scale=8.0, 
            width=512, 
            height=512, 
            samples=1, 
            sampler=generation.SAMPLER_K_DPMPP_2M)
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    return_dict["completion"] = True
                    return_dict["message"] = """Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."""
                    return return_dict
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img_bytes = io.BytesIO(artifact.binary)
                    img = Image.open(img_bytes)
                    img.save("/tmp/" + str(artifact.seed)+ ".png")
                    # img.save(str(artifact.seed)+ ".png") 
                    img_bytes.seek(0)
                    bucket_name = bucket
                    key = "/tmp/" + str(artifact.seed)+ ".png"
                    # key = str(artifact.seed)+ ".png"  
                    s3.upload_file(key,bucket,str(artifact.seed)+ ".png",ExtraArgs={'ACL': 'public-read', 'ContentType': "image/jpg, image/png, image/jpeg"})
                    return_dict["completion"] = True
                    return_dict["message"] = "Successful upload"
                    return_dict["url"] = "https://picturebucket133234-dev.s3.amazonaws.com/" + str(artifact.seed)+ ".png"
                    print(return_dict["url"])
                    return return_dict
    except Exception as e:
        return_dict["message"] = e
        return return_dict
    