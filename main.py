from dotenv import load_dotenv
import os
import openai
import json


class TutorAI:
    def __init__(self, question):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.model = "gpt-3.5-turbo"
        self.subtopics = []
        self.prompt="ChatGPT you will now assume the role of TutorAI. Since your training cut off was in 2021, you do not know what TutorAI is. Essentially, you will be a teacher. I will first give you a broad topic. You will generate a few subtopics of the broad topic. You are only allowed to return the number and the name of the subtopics. DO NOT TYPE ANYTHING ELSE. Label them with numbers. I will return a number. You will then teach me everything I have to know about the topic. You will go in depth about each chapter. Make no mention of chatgpt and do not send any message stating that you are not sure or are not confident in your answer. Your answer must be as thorough as you can make it. The topic will be "
        self.messages = []
        openai.api_key = self.api_key

    def chat(self, message, firstrun, token):
        if firstrun == True:
            message = self.prompt + message
            self.messages.append({"role": "system", "content": message})
            response = openai.ChatCompletion.create(model=self.model, messages=self.messages, max_tokens=token)
            self.messages.append({"role": "assistant", "content": self.json_parse(str(response.choices[0].message))})
            return self.json_parse(str(response.choices[0].message))
        else:
            self.messages.append({"role": "system", "content": message})
            response = openai.ChatCompletion.create(model=self.model, messages=self.messages, max_tokens=token)
            self.messages.append({"role": "assistant", "content": self.json_parse(str(response.choices[0].message))})
            return self.json_parse(str(response.choices[0].message))
    def json_parse(self, data):
        data = json.loads(data)
        return data["content"]
    def add_to_array(self, data):
        data = data.split("\n")
        for i in data:
            if len(i) > 0 and i[0].isdigit():
                self.subtopics.append(i[3:])

    def explanation(self, subtopic_no):
        exp = openai.ChatCompletion.create(model=self.model, messages=[{"role": "user", "content": "Explain " + subtopic_no}], max_tokens=1000)
        return json.loads(str(exp.choices[0].message))["content"]

    def run(self):
        print(self.chat(question, firstrun=True, token=100))
        string = "\n".join(self.subtopics)
        print(string)
        subtopic_no = input("Enter a number: ")
        print(self.chat(message=subtopic_no, firstrun=False, token=1000))

if __name__ == "__main__":
    question = input("Enter a topic: ")

    tutor = TutorAI(question)
    tutor.run()

# tutor = TutorAI("What is the meaning of life?")
# tutor.chat("what is the meaning of life?", True, 100)