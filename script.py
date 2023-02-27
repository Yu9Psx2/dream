def dream_request(phrase):

    import os
    import os
    import io
    import warnings
    from PIL import Image
    from stability_sdk import client
    import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
    import boto3

    #Code is modified from dream studio example found at: https://platform.stability.ai/docs/getting-started/authentication

    return_dict = {"completion": False,
                "url": None,
                "message":None,
                }

    try:

        access_key=os.environ.get('REACT_APP_accessKeyId')
        secret_key=os.environ.get('REACT_APP_secretAccessKey')
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
                    return_dict["message"] = """Your request activated the API's safety filters and could not be processed.
                        Please modify the prompt and try again."""
                    return return_dict
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img_bytes = io.BytesIO(artifact.binary)
                    img = Image.open(img_bytes)
                    img.save(str(artifact.seed)+ ".png") 
                    img_bytes.seek(0)
                    bucket_name = bucket
                    key = str(artifact.seed)+ ".png"  
                    s3.upload_file(key,bucket,key,ExtraArgs={'ACL': 'public-read', 'ContentType': "image/jpg, image/png, image/jpeg"})
                    return_dict["completion"] = True
                    return_dict["message"] = "Successful upload"
                    return_dict["url"] = "https://picturebucket133234-dev.s3.amazonaws.com/" + key
                    print(return_dict["url"])
    except:
        return return_dict
    

dream_request("expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli")