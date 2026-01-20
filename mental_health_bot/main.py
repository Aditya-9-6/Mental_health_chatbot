import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from ui import setup_ui
from utils import load_knowledge_base, get_vector_store, check_safety
from constants import CRISIS_RESPONSE, PROMPT_TEMPLATE
from database import create_tables
from logging_config import get_logger

logger = get_logger(__name__)

def main():
    # Create database and tables if they don't exist
    create_tables()
    logger.info("Database tables created or already exist.")

    # Load environment variables
    current_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(current_dir, '.env'))
    logger.info("Environment variables loaded.")

    # Page Config
    setup_ui()

    config_path = os.path.join(current_dir, 'config.yaml')
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
        logger.info(f"User '{username}' logged in successfully.")
        
        # Main app logic goes here
        # Safety Guardrails
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Setup API Key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # Try st.secrets
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
            else:
                api_key = st.sidebar.text_input("Enter Google API Key", type="password")

        if not api_key:
            st.warning("Please provide a Google API Key to continue.")
            st.stop()

        # Main Logic
        docs = load_knowledge_base()
        vector_store = get_vector_store(docs, api_key)
        logger.info("Knowledge base and vector store loaded.")

        if vector_store:
            # Setup LLM and Chain
            llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.3)
            
            PROMPT = PromptTemplate(
                template=PROMPT_TEMPLATE, input_variables=["context", "question"]
            )
            
            chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
                chain_type_kwargs={"prompt": PROMPT}
            )
            logger.info("LLM and QA chain initialized.")

            # Chat Interface
            if prompt := st.chat_input("How are you feeling today?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                logger.info(f"User '{username}' sent a new message: {prompt}")

                # Safety Check
                if not check_safety(prompt):
                    response = CRISIS_RESPONSE
                    logger.warning(f"Crisis keyword detected in user input: {prompt}")
                else:
                    with st.spinner("Thinking..."):
                        try:
                            result = chain.invoke({"query": prompt})
                            response = result['result']
                            logger.info(f"LLM generated a response: {response}")
                        except Exception as e:
                            response = f"I'm sorry, I encountered an error: {e}"
                            logger.error(f"An error occurred while generating a response: {e}")

                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)

    elif authentication_status == False:
        st.error('Username/password is incorrect')
        logger.warning(f"Failed login attempt for username: {username}")
    elif authentication_status == None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()
