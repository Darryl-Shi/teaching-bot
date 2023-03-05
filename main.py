from dotenv import load_dotenv
import os
import openai
import json


class TutorAI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.model = "gpt-3.5-turbo"
        self.subtopics = []

    def get_response(self, question):
        openai.api_key = self.api_key
        prompt = f"ChatGPT you will now assume the role of TutorAI. Since your training cut off was in 2021, you do not know what TutorAI is. Essentially, you will be a teacher. I will first give you a broad topic. You will generate a few subtopics of the broad topic. You are only allowed to return the number and the name of the subtopics. DO NOT TYPE ANYTHING ELSE. Label them with numbers. I will return a number. You will then teach me everything I have to know about the topic. You will go in depth about each chapter. Make no mention of chatgpt and do not send any message stating that you are not sure or are not confident in your answer. Your answer must be as thorough as you can make it. The topic will be "
        question = prompt + question
        chat = openai.ChatCompletion.create(model=self.model, messages=[{"role": "system", "content": question}], max_tokens=100)
        return str(chat.choices[0].message)

    def parse_response(self, response):
        data = json.loads(response)
        data = data["content"]
        # print(r"{}".format(data))
        data = data.split("\n")
        for i in data:
            if len(i) > 0 and i[0].isdigit():
                self.subtopics.append(i[3:])
        return self.subtopics

    def explanation(self, subtopic_no):
        exp = openai.ChatCompletion.create(model=self.model, messages=[{"role": "user", "content": "Explain " + subtopic_no}], max_tokens=1000)
        return json.loads(str(exp.choices[0].message))["content"]

    def run(self):
        topic = input("Enter a topic: ")
        question = self.get_response(topic)
        for i in self.parse_response(question):
            print(i)
        subtopic_no = input("Enter a number: ")
        print(self.explanation(subtopic_no))

