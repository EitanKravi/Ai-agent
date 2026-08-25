import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import argparse

from prompts import system_prompt
from call_function import available_functions, call_function


def chat_respond(client, messages: list[dict], args):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    # Give error if didn't get response
    if response.usage.completion_tokens is None:
        raise RuntimeError()

    # print info about the response and the user prompt
    if args.verbose:
        print("User prompt: ", args.user_prompt)

        print("Prompt tokens: ", response.usage.prompt_tokens)
        print("Response tokens: ", response.usage.completion_tokens)

    # print the response
    if response.choices[0].message.content is not None:
        print("Response:")
        print(response.choices[0].message.content)

    # Catching what tool to use
    message = response.choices[0].message

    # add message to messages
    messages.append(message)

    if message.tool_calls is not None and len(message.tool_calls) > 0:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if args.verbose:
                print(f"-> {result_message['content']}")

            # add the result of the call_function to messages
            messages.append(result_message)

        # To continue the loop
        return True
    else:
        # To end the loop when there is no more tool_calls
        return False

def main():
    # Get API key
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    # Give an error if a .env file containing the OPENROUTER_API_KEY key is not found.
    if api_key is None:
        raise RuntimeError("API key wasn't found")

    # Accept a command-line argument when running the script, in order to pass it to the AI agent
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    # Set the AI agent
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    run: bool = True
    get_final_result: bool = False

    # Get response from the AI agent
    for _ in range(20):
        run = chat_respond(client, messages, args)
        if not run:
            get_final_result = True
            break

    if not get_final_result:
        print("Maximum number of runs reached and not receive final response")
        exit(1)



if __name__ == "__main__":
    main()

