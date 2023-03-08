import os
import openai
import json
import random


def access_api(prompt=None, messages=None,user_response = None, good_flag = True, iterator = 0):
#Get API key and setup the options list
    openai.api_key = os.getenv("OPENAI_API_KEY")
    options = []
    options2= {}
    end_flag = False
#If this is the first time the script is run for the user, access the script using the initiating prompt.
    if not messages:
            messages = [{"role": "system", "content": "You are a choose your own adventure book. When you present a decision point you should offer two or three possibilities, and put each of the possibilities on a its own new line so that I can parse the response. Make sure to label these options such as Option A, Option B, Option C. Write 'the end' on a new line when the story is over so that I can parse it"},
            {"role": "user", "content": f"Write a choose-your own adventure story about {prompt}. For this prompt, provide me with the opening of the story to the first decision point. Remember you should offer two or three possibilities, and put each of the possibilities on its own new line so that I can parse the response. Make sure to label these options such as Option A, Option B, Option C."},]
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
#If this is the subsequent times the script is run for the user, access the script using the built up messages.
    else:
#ChatGPT tends not to introduce downside to the story, so we introduce an element of chance that the story goes wrong
        outcome = ""            
        if good_flag == True:
            outcome = ". The story should take an unexpectedly negative path in your response." if (random.randint(0,10) > 7) else ""
            good_flag == False
        elif good_flag == False:
            outcome = ". The story should return to a positive path in your response." if (random.randint(0,10) > 3) else ""
            good_flag == True
        user_response += outcome
        if iterator == 5:
            user_response = user_response + "End the story in your next response and don't provide any more options"
        messages.append({"role":"user","content":user_response})
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
    messages.append({"role":role,"content":content})
    if "THE END" in content.split('\n')[-1].upper() or "THE END" in content.split('\n')[-1].upper():
        end_flag = True
    if len(options) == 0:
         end_flag = True
    iterator += 1
    outgoing_response = [messages, options2, iterator, good_flag, end_flag]
    return outgoing_response

