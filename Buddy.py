import streamlit as st
from openai import OpenAI
import json
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


MEMORY_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


if "messages" not in st.session_state:
    st.session_state.messages = load_memory()


st.set_page_config(page_title="Buddy AI", page_icon="🤖")
st.title("🤖 Buddy – Assistant IA")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Pose ta question à Buddy..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es Buddy, un assistant intelligent, clair et pédagogique."}
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

    # Sauvegarder mémoire
    save_memory(st.session_state.messages)
