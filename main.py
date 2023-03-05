from dotenv import load_dotenv
import os
import openai
import json


class TutorAI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.subtopics = []
        self.messages = []
        self.token = int(os.getenv("TOKEN"))
        self.prompt_stages = ["A student wants to learn about a topic, generate 4 modules that a student can use to learn and number it. A module consists of a title and a description, separated by a colon. The topic is ", "Create an outline with 4 sections for teaching a student about the topic and module and number it. If you receive the input 'back', go back to the previous stage.","Teach a student about the below topic and subtopic and by writing multiple paragraphs and number it. If you receive the input 'back', go back to the previous stage"]
        self.topic = ""
        openai.api_key = self.api_key

    def add_topic(self, topic):
        self.prompt_stages[0] = self.prompt_stages[0]+topic
    def chat(self, stage):
        self.messages.append({"role": "user", "content": str(self.prompt_stages[stage])})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.token,
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    
    def run(self):
        self.topic = input("Topic: ")
        self.add_topic(self.topic)
        i=1  # start at stage 1
        print(self.chat(i))  # convert stage number to string before passing to chat method
        while True:
            user_input = input("Type 'next' to go to the next stage or 'exit' to exit:")
            if user_input == "exit":
                break
            if user_input == "next":
                i += 1
                print(self.chat(i))
            else:
                print(self.chat(i))  # also convert stage number to string here


if __name__ == "__main__":
    tutor = TutorAI()
    tutor.run()
