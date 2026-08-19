import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

st.set_page_config(page_title="Bitte Menu RAG", page_icon=":robot:", layout = 'centered')
st.title("Bitte Menu RAG")
st.markdown('Your intelligent Bitte RAG system')
st.divider()

with st.expander("About this web app"):
    st.write("""
    Bitte RAG Chatbot

- Model: gpt-5 via OpenAI Responses API
- RAG: File Search tool using your pre-built Vector Store
- Features: multi-turn chat, image inputs, clear conversation
- Secrets: reads OPENAI_API_KEY and VECTOR_STORE_ID from Streamlit secrets or environment variables

How it works
Your message and (optional) images go to the Responses API along with a system prompt.
""")

openai_api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("VECTOR_STORE_ID")
client = OpenAI(api_key=openai_api_key)

st.write(f"API key loaded: {bool(openai_api_key)}")
st.write(f"Vector store ID: {vector_store_id}")

system_prompt = 'you are a helpful assistant that can answer questions and help with tasks. Use information from the vector store only. If you cant find information, say you didnt find. '
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'previous_response_id' not in st.session_state:
    st.session_state.previous_response_id = None


if not openai_api_key:
    st.warning("OPENAI_API_KEY is not set")

if not vector_store_id:
    st.warning("VECTOR_STORE_ID is not set")

with st.sidebar:
    st.header('User Controls')
    st.divider()

    if st.button('Clear Conversation'):
        st.session_state.messages = []
        st.session_state.previous_response_id = None
        st.rerun()


uploaded = st.file_uploader(
    'Upload a file',
    type = ['pdf', 'jpeg', 'jpg', 'webp'],
    accept_multiple_files = True,
)


#Helper function to input parts:

def build_input_parts(text, images):
    content = []
    if text and text.strip():
        content.append({"type": "input_text", "text": text.strip()})

    for img in images:
        content.append({
            'type': 'input_image',
            'image_url': img['data_url'],
            'detail': 'auto' 
        })

    return [
        {'role': 'developer', 'content': system_prompt},
        {'role': 'user', 'content': content}
    ]

def generate_response(messages, previous_response_id):
    return client.responses.create(
        model = "gpt-5-nano",
        input = messages,
        previous_response_id = previous_response_id,
        tools = [{
            'type': 'file_search',
            'vector_store_ids': [vector_store_id],
            'max_num_results' : 10}]
    )       

def get_output(response):
    return response.output_text


images = []
prompt = st.chat_input('Enter your prompt')

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:
    if uploaded:
        for file in uploaded:
            if file.type:
                extension = file.type.split('/')[1]
                mime_type = f"image/{extension}"
            else:
                mime_type = 'image/png'

            image_bytes = file.read()
            encoded_bytes = base64.b64encode(image_bytes)
            encoded_string = encoded_bytes.decode('utf-8')

            data_url = f"data:{mime_type};base64,{encoded_string}"
            image_dict = {
                "mime_type": mime_type,
                "data_url": data_url
            }
            images.append(image_dict)
        
    parts = build_input_parts(prompt, images)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)

    with st.chat_message('assistant'):
        with st.spinner('Thinking'):
            
            response = generate_response(parts,st.session_state.previous_response_id)
            output = get_output(response)
            st.markdown(output)
            st.session_state.previous_response_id = response.id
            st.session_state.messages.append({'role': 'assistant', 'content': output})







