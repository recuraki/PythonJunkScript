import webvtt
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import (AIMessage, HumanMessage, SystemMessage)
import os
os.environ["OPENAI_API_KEY"] = "xxx"
chat = ChatOpenAI(temperature=0, verbose=True)

vtt = webvtt.read('test.vtt')
print("Read {} sentenses".format(len(vtt)))
memory = []
cur = []
for i in range(len(vtt)):
    x = vtt[i]
    text = x.text
    wordcnt = x.text.split()
    batch_messages = [
        [
            SystemMessage(content="次のすべての英語を日本語にしてください。"),
            HumanMessage(content=x.text)
        ],
    ]
    result = chat.generate(batch_messages)
    jpstr = ""
    for x in result.generations: jpstr += x[0].text
    print("<- {}".format("You are a helpful assistant that translates English to Japanese. - " + text))
    print("-> {}".format(jpstr))
    print(result.llm_output)
    vtt[i].text = jpstr

with open('my_captions.vtt', 'w') as fd:
    vtt.write(fd, format="vtt")