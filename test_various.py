import os
import openai
import json
import random
import time

openai.api_key = os.getenv("OPENAI_API_KEY")


# prompt = ["A day in the life of a camel in Egypt", "a day in the life of a robot waiter", "A day in the life of a roof shingle", "A day in the life of an accountant", "A day at the museum", "A day at the science fair"]
prompt = ["A day at the beach", "A day at the museum"]
for i in prompt:
    time.sleep(10)
    options = []
    options2= {}
    messages = [{"role": "system", "content": """You are a choose your own adventure book. When you present a decision point you should offer two or three possibilities, and put each of the possibilities on a its own new line so that I can parse the response. Make sure to label these options such as Option A, Option B, Option C. Write 'the end' on a new line when the story is over so that I can parse it. An example of a correctly formatted response is: You are hiking in the woods, enjoying the beautiful scenery around you when suddenly you hear a rustling in the bushes. You turn to see a massive bear charging in your direction. Your heart racing, you have to think fast. What will you do?

Option A: Climb the nearest tree to try and get out of reach of the bear.
Option B: Stand completely still and hope that the bear will lose interest and leave.
Option C: Head towards the nearest body of water in hopes of confusing the bear."""},
        {"role": "user", "content": f"""Write a choose-your own adventure story about {i}. For this prompt, provide me with the opening of the story to the first decision point. Remember you should offer two or three possibilities, and put each of the possibilities on its own new line so that I can parse the response. Make sure to label these options such as Option A, Option B, Option C. An example of a correctly formatted response is: You are hiking in the woods, enjoying the beautiful scenery around you when suddenly you hear a rustling in the bushes. You turn to see a massive bear charging in your direction. Your heart racing, you have to think fast. What will you do?

Option A: Climb the nearest tree to try and get out of reach of the bear.
Option B: Stand completely still and hope that the bear will lose interest and leave.
Option C: Head towards the nearest body of water in hopes of confusing the bear."""}]
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages)
    response_json_str = json.dumps(response.to_dict())
    response_json = json.loads(response_json_str)
    message = response_json['choices'][0]['message']
    content = message['content']
    role = message['role']
        # print(content)
    for i in content.split('\n')[1:]:
            if "Option" in i:
                    options.append(i)
    # print(f"This is options {options}")
    for i in options:
            options2[i] = '' 
    # print(options2)
    print(content)
