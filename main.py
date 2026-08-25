import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import argparse

from prompts import system_prompt
from call_function import available_functions, call_function


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

    # Get response from the AI agent
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
    print("Response:")
    print(response.choices[0].message.content)

    # Catching what tool to use
    message = response.choices[0].message

    if message.tool_calls is not None and len(message.tool_calls) > 0:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if args.verbose:
                print(f"-> {result_message['content']}")




if __name__ == "__main__":
    main()

