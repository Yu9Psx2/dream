from lambda_function import lambda_handler

holder = lambda_handler(event = {"phrase":"a day at buckingham",
                        "story": {
                            "returned_messages":None,
                            "returned_good_flag":None,
                            "returned_iterator":0,
                            "user_response":None,
                        }                        
                        }, context = None)

returned_messages = holder['story']['returned_messages']
returned_iterator = holder['story']['returned_iterator']
returned_good_flag = holder['story']['returned_good_flag']

holder2 = lambda_handler(event = {"phrase":"a day at buckingham",
                        "story": {
                            "returned_messages":returned_messages,
                            "returned_good_flag":None,
                            "returned_iterator":returned_iterator,
                            "user_response":"option B",
                        }                        
                        }, context = None)