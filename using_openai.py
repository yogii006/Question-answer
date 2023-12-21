# python 3.8 (3.8.16) or it doesn't work
# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    # openai_api_key="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"
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == " ":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    # setup streamlit page
    st.set_page_config(
        page_title="Hello world",
        page_icon="chart_with_upwards_trend",
        layout="wide",

    )


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.header("Your own ChatGPT 👨🏻‍⚖️")

    # sidebar with user input
    container1 = st.container(border=True)
    container2 = st.container(border=True)
    with container1:
        user_input = st.text_input("Your message: ", key="user_input")

        # handle user input
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))
            user_input = ''

    # display message history
    with container2:
        messages = st.session_state.get('messages', [])
        for i, msg in enumerate(messages[1:]):
            if i % 2 == 0:
                message(msg.content, is_user=True, key=str(i) + '_user')
            else:
                message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()