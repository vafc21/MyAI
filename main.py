from openai import OpenAI
import json
from datetime import datetime
from dotenv import load_dotenv
import os

class Jarvis:
    def __init__(self):
        self.name = "Jarvis"
        load_dotenv()
        self.client = OpenAI(api_key=str(os.getenv("OPENAI_API_KEY")))

    def get_current_time(self, location):
        # Simulated function logic
        return f"The current time in {location} is {datetime.now().strftime('%H:%M:%S')}"

    def gpt_response(self, prompt):
        functions = [
            {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        }
                    },
                    "required": ["location"]
                }
            }
        ]

        messages = [
            {"role": "system", "content": "You are an assistant that can check time."},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=functions,
            tool_choice="auto"
        )

        assistant_msg = response.choices[0].message

        if assistant_msg.tool_calls:
            call = assistant_msg.tool_calls[0]
            func_name = call.function.name
            args = json.loads(call.function.arguments)

            if func_name == "get_current_time":
                result = self.get_current_time(location=args["location"])
            else:
                result = "Function not implemented."

            messages.append(assistant_msg)
            messages.append({
                "role": "tool",
                "name": func_name,
                "content": result
            })

            final = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            return final.choices[0].message.content
        else:
            return assistant_msg.content

# Run the assistant
if __name__ == "__main__":
    jarvis = Jarvis()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = jarvis.gpt_response(user_input)
        print(f"{jarvis.name}: {response}")
