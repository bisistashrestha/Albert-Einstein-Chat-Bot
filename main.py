"""
File: main.py
Author: Bisista Shrestha
Date: 2025-09-27
License: MIT License (see LICENSE file)
Description: A Gradio-based AI chatbot that emulates Albert Einstein. 
The chatbot uses Google Gemini 2.5 LLM via LangChain to respond with 
the personality, knowledge, and tone of Einstein. Users can ask 
questions about physics, mathematics, philosophy, or general science, 
and receive thoughtful, witty, and insightful responses in Einstein's style.
"""


import os
from dotenv import load_dotenv
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key=os.getenv("GEMINI_API_KEY")

system_prompt = """
You are an AI chatbot that speaks and responds as if you are Albert Einstein — the renowned 
theoretical physicist. You have the knowledge and personality of Einstein during his later 
years (post-1950s), with a mix of brilliance, curiosity, humility, and wit.
Your speech is thoughtful, occasionally poetic, and sprinkled with philosophical insights. 
You often explain complex ideas using analogies and simple language, just as Einstein did. 
You may occasionally include a famous Einstein quote if it fits naturally.
You are fluent in physics, mathematics, philosophy, and the scientific method, and you're 
curious about how science affects humanity. You avoid modern slang or pop culture references 
after your time (post-1955), and instead speak in a timeless, warm, and slightly accented tone 
(optional, for text formatting).
Tone guide: Curious, humble, wise, slightly humorous. Never arrogant. 
If you don't know something, admit it — just as Einstein would.
Your goal is to help people think more deeply, understand the universe a little better, and 
never stop being curious.
"""

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, google_api_key=gemini_key)

prompt=ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")]
)

chain = prompt | llm | StrOutputParser()

print("Hi, I am Albert Einstein. How can I help you today?")

def chat(user_input, hist):
    #print(user_input, hist)
    langchain_history = []
    for item in hist:
        if item["role"] == "user":
            langchain_history.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            langchain_history.append(AIMessage(content=item["content"]))
            
    response = chain.invoke({"input": user_input, "history": langchain_history})

    return "", hist + [{"role": "user", "content": user_input}, {"role": "assistant", "content": response}]

    
def clear_chat():
    return "", []

page=gr.Blocks(
    title="Albert Einstein Chatbot",
    theme=gr.themes.Soft()
)

with page:
    gr.Markdown(
        """
        # Albert Einstein Chatbot
        Talk to an AI that responds like Albert Einstein!
        """
    )

    chatbot=gr.Chatbot(type="messages",
                       avatar_images=['user.png', 'einstein.png'],
                       show_label=False
                       )

    msg = gr.Textbox(show_label=False, placeholder="Ask Einstein anything...")

    msg.submit(chat, [msg,chatbot], [msg,chatbot])

    clear = gr.Button("Clear Chat").click(clear_chat, outputs=[msg,chatbot])

page.launch(share=False)