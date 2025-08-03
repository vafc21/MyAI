from openai import OpenAI
import json
from datetime import datetime
from dotenv import load_dotenv
import os

class Jarvis:
    def __init__(self):
        self.name = "Jarvis"

        # Load API key from .env
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENROUTER_API_KEY in .env")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        # Load function definitions from JSON file
        try:
            with open("functions.json", "r") as f:
                self.tools = json.load(f)
        except:
            print("⚠️ No fuctons found in functions.json, using default tools. ⚠️")

    def get_current_time(self, location):
        return f"The current time in {location} is {datetime.now().strftime('%H:%M:%S')}"

    def gpt_response(self, prompt):
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Please answer the user's questions and use tools when necessary. Only use futions when needed. Do not tell the user about your tools only if needed use them."},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        assistant_msg = response.choices[0].message

        if assistant_msg.tool_calls:
            call = assistant_msg.tool_calls[0]
            func_name = call.function.name
            args = json.loads(call.function.arguments)

            if func_name == "get_current_time":
                result = self.get_current_time(args["location"])
            else:
                result = "Function not implemented."

            messages.append({"role": "assistant", "tool_calls": [call]})
            messages.append({"role": "tool", "name": func_name, "content": result})

            final = self.client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=messages
            )
            return final.choices[0].message.content
        else:
            return assistant_msg.content

# Run the assi
if __name__ == "__main__":
    jarvis = Jarvis()
    print("Jarvis is ready. Type something or 'exit' to quit.\n")  # ✅ Add this line

    while True:
        user_input = input("You: ")  # If nothing shows, maybe stdin isn't working
        if user_input.strip() == "":
            print("⚠️ Empty input. Please type something.")
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("🔄 Thinking...")
        try:
            response = jarvis.gpt_response(user_input)
            print(f"{jarvis.name}: {response}")
        except Exception as e:
            print("❌ Error:", e)
