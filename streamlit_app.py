import openai
import streamlit as st

# Configuração da barra lateral
with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')

    # Verifica se a chave da API está nos segredos
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        # Solicita ao usuário a chave da API
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Coleta o prompt do usuário
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepara a mensagem de resposta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Chama a API da OpenAI para obter a resposta
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True  # Habilita o streaming de respostas
            )

            # Processa as respostas no modo streaming
            for chunk in response:
                delta_content = chunk.choices[0].delta.get("content", "")
                full_response += delta_content
                message_placeholder.markdown(full_response + "▌")  # Exibe a resposta parcial
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        # Exibe a resposta final
        message_placeholder.markdown(full_response)

    # Armazena a resposta do assistente no histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
