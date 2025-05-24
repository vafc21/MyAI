import speech_recognition as sr
import pyttsx3
import requests
import smtplib
import datetime
import webbrowser
import tkinter as tk
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import gpt_api


class MyAI:
    def __init__(self):
        self.name = "Jarvis"
        self.usingText = True
        self.onWhat = ''
        self.conversation_history = []  
        if self.onWhat.lower() == "pc":
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
            self.model_name = "EleutherAI/gpt-neo-1.3B"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16).cuda()
            self.tokenizer.pad_token = self.tokenizer.eos_token
        else:
            self.client = OpenAI(api_key=gpt_api.api)
            

    def speak(self, text):
        if self.usingText==True:
            print(text)
        else:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self):
        if self.usingText==True:
            return input('You:')
        else:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
                try:
                    command = r.recognize_google(audio)
                    print(f"You said: {command}")
                    return command.lower()
                except sr.UnknownValueError:
                    print("Sorry, I did not understand that.")
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None

    def get_online_gpt_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using GPT-3.5-turbo instead of GPT-4
                messages=[
                    {"role": "system", "content": f"Your name is {self.name}. You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return "I apologize, but I encountered an error. Please try again."

    def get_local_gpt_response(self, prompt):
        
        self.conversation_history.append({"role": "user", "content": prompt})

        
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
        inputs = self.tokenizer(context, return_tensors="pt", padding=True).to("cuda")

        
        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=300,
            temperature=0.7,
            do_sample=True
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Add the assistant's response to the conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def start(self):
        self.speak(f"Hello, my name is {self.name}. How can I help you today?")
        while True:
            command = self.listen()
            if command:
                if "open google" in command:
                    webbrowser.open("https://www.google.com")
                    self.speak("Opening Google.")
                elif "what time is it" in command:
                    now = datetime.datetime.now()
                    current_time = now.strftime("%H:%M")
                    self.speak(f"The current time is {current_time}.")
                elif "send email" in command:
                    self.speak("What is the recipient's email address?")
                    recipient = self.listen()
                    self.speak("What is the subject of the email?")
                    subject = self.listen()
                    self.speak("What is the message?")
                    message = self.listen()
                    self.send_email(recipient, subject, message)
                else:
                    isonWhat = self.onWhat.upper()
                    if isonWhat == "PC":
                        response = self.get_local_gpt_response(command)
                    else:
                        response = self.get_online_gpt_response(command)
                    self.speak(response)

                    # Check if the assistant wants to continue the conversation
                    if "continue" in response.lower():
                        self.speak("What else can I help you with?")
                    else:
                        self.speak("Goodbye!")
                        break
            else:
                self.speak("I didn't catch that. Can you repeat?")
AI = MyAI()
AI.start()





