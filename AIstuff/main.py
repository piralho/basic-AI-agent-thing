#import all the things were gonna need
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_FUNC_CALLS

import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
import json

#I'm preeetty sure "load enviroment" just means take the envelope thing like in linux so that all the dependences are here without needing to download it to evey folder and so that you can just run it from a git download instead of needing to download all the dependences(like the things I import there ^^^) 
load_dotenv()

#set wheremstve the helle I will aquire the doomsday devide refered by the commonwealth as "generative AI model"
api_key = os.environ.get("OPENROUTER_API_KEY")

#makin' sure api_key isn't a pile of bullshit
if not api_key:
    raise RuntimeError("API key was not compatible with code/inputed incorrectly.")

#initiate a client object from the OpenAI class 
client:object = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)

#initiate parser from argument parser
#basicaly this just lets me write stuff in the command line and have it easily put into a variable
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

#makes a list that will be used to keep track of the messages (I finks)
messages = [{"role":"system", "content":system_prompt},
            {"role":"user", "content":args.user_prompt}]



#this gets the response of the AI as a "chat completion object"(whatever that is)
#apparently to actually access the text I have to use response.choices[0].message.content so response is probably a bunch of garbage data about the ai or smth idk
response = client.chat.completions.create(model="openrouter/free",
                                          messages=messages,
                                          tools = available_functions,)

#check if response.usage isn't a bowl of bulliard shit
if not response.usage:
    raise RuntimeError("The responses 'usage' property is NoneType. Please retry and if that doesn't fix it perform your best ostrich impression!")


#makes it so that if the user want is verbose we give them the verbosses (just shows like how much "tokens" were spent but idrk how that even works)
if args.verbose:
    print(f"User prompt:{args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")


#make sure it doesn't just go into an infinite loop by limitin' the amount of functions it can calls 
for _ in range(MAX_FUNC_CALLS):

    response = client.chat.completions.create(model="openrouter/free",messages=messages,tools = available_functions,)

    #append the next thing the ai wants to do to the list
    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for call in message.tool_calls:
            result_message = call_function(call, args.verbose)
            if not result_message["content"]:
                raise Exception("results from the function call were null")
            if args.verbose:
                print(f"-> {result_message['content']}")
            else:
                print(result_message["content"])
            #append the tool call to the messages list
            messages.append(result_message)
    else:
        print(message.content)
        sys.exit(0)

#in case we run out of func calls
print("Max amount of func calls reached please retry in case this was an accidental recursion loop or increase the MAX_FUNC_CALLS variable in config.py")
sys.exit(1)




