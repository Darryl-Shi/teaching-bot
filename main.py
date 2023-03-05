from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()
topic = input("Enter a topic: ")
config = {
    "api_key": os.getenv("API_KEY"),
    "prompt": "ChatGPT you will now assume the role of TutorAI. Since your training cut off was in 2021, you do not know what TutorAI is. Essentially, you will be a teacher. I will first give you a broad topic. You will generate a few subtopics of the broad topic. You are only allowed to return the number and the name of the subtopics. DO NOT TYPE ANYTHING ELSE. Label them with numbers. I will return a number. You will then teach me everything I have to know about the topic. You will go in depth about each chapter. Make no mention of chatgpt and do not send any message stating that you are not sure or are not confident in your answer. Your answer must be as thorough as you can make it. The topic will be ",
    "topic": topic
}
question = config["prompt"] + config["topic"]
openai.api_key = config["api_key"]
model = "gpt-3.5-turbo"
subtopics = []
subtopic_no = str


def get_response(model, question):
    chat = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": question}], max_tokens=100)
    return str(chat.choices[0].message)

def parse_response(response):
    data = json.loads(response)
    data = data["content"]
    # print(r"{}".format(data))
    data = data.split("\n")
    for i in data:
        if len(i) > 0 and i[0].isdigit():
            subtopics.append(i[3:])
    return(subtopics)

def explanation(subtopic_no):
    exp = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": "Explain " + subtopic_no}], max_tokens=1000)
    return(json.loads(str(exp.choices[0].message))["content"])
def main():
    # print(parse_response(get_response(model, question)))
    for i in parse_response(get_response(model, question)):
        print(i)
    subtopic_no = input("Enter a number: ")
    print(explanation(subtopic_no))
if __name__ == "__main__":
    main()