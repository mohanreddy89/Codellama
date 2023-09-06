import streamlit as st

import replicate

import os

 

# App title

st.set_page_config(page_title="llama2 ")

 

# Replicate Credentials

with st.sidebar:

    st.title('llama2')

    if 'REPLICATE_API_TOKEN' in st.secrets:

        st.success('API key already provided!')

        replicate_api = st.secrets['REPLICATE_API_TOKEN']

    else:

        replicate_api = st.text_input('Enter Replicate API token:', type='password')

        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):

            st.warning('Please enter your credentials!')

        else:

            st.success('Proceed to entering your prompt message!')

 


    

    st.markdown("llama")

os.environ['REPLICATE_API_TOKEN'] = replicate_api

 

# Store LLM generated responses

if "messages" not in st.session_state.keys():

    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

 

# Display or clear chat messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

 

def clear_chat_history():

    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

 

# Function for generating LLaMA2 response

 

def generate_llama2_response(prompt_input):

    

    string_dialogue = """

    You are a coding assistant.

 

   

      Respond as the 'Assistant' only and refrain from impersonating the 'User'.

When providing a code answer, wrap the code using triple backticks (```).
If you're unsure or don't have the information, please acknowledge that you don't know and avoid speculating.
Keep your response brief, directly addressing the question at hand, and ensure its relevance.

    """

    

    for dict_message in st.session_state.messages:

        if dict_message["role"] == "user":

            string_dialogue += "User: " + dict_message["content"] + "\n\n"

        else:

            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    #output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',

    output = replicate.run('replicate/codellama-7b-instruct:0103579e86fc75ba0d65912890fa19ef03c84a68554635319accf2e0ba93d3ae',

                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",

                                    "repetition_penalty":1.15})

    return output

 

# User-provided prompt

if prompt := st.chat_input(disabled=not replicate_api):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):

        st.write(prompt)

 

# Generate a new response if last message is not from assistant

if st.session_state.messages[-1]["role"] != "assistant":

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = generate_llama2_response(prompt)

            placeholder = st.empty()

            full_response = ''

            for item in response:

                full_response += item

                placeholder.markdown(full_response)

            placeholder.markdown(full_response)

    message = {"role": "assistant", "content": full_response}

    st.session_state.messages.append(message)