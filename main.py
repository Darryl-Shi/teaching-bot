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
        self.prompt=os.getenv("PROMPT")
        self.messages = []
        self.token = int(os.getenv("TOKEN"))
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
        while True:
            subtopic_no = input("Enter a number or ask a question(or exit to quit): ")
            if subtopic_no == "exit":
                break
            print(self.chat(message=subtopic_no, firstrun=False, token=self.token))

if __name__ == "__main__":
    question = input("Enter a topic: ")

    tutor = TutorAI(question)
    tutor.run()