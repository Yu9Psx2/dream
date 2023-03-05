from chat_gpt_call import access_api

user_input = input("give us a story prompt")
returned_messages, returned_options, returned_iterator, returned_good_flag, returned_end_flag = access_api(prompt=user_input, messages=None,user_response = None, good_flag = True, iterator = 0)
while returned_end_flag == False:
    user_input = input()
    returned_messages, returned_options, returned_iterator, returned_good_flag, returned_end_flag = access_api(prompt=None, messages=returned_messages,user_response = user_input, good_flag = returned_good_flag, iterator = returned_iterator)
