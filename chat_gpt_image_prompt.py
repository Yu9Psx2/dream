import os
import openai
import json


def get_image_prompt(story,option, style = "anime"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [{"role": "system", "content": "You are a helpful assistant that is helping the user generate a prompt to use to create images in the front-end of an image generation model"},
    {"role": "user", "content": f"I am writing a choose your own adventure story. The story on this page is {story} and the option presented to the user is {option}. Please write me a short description of the option that I can feed into an image generator to use as an image for this particular option. Ask it to do it in the style of {style}. Your response must be less than 480 characters, so just respond with the prompt that I am going to feed into the generator, I do not need any introductory or concluding remarks"},]
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages)
    response_json_str = json.dumps(response.to_dict())
    response_json = json.loads(response_json_str)
    message = response_json['choices'][0]['message']
    content = message['content']
    content = content + "in anime style"
    return content
