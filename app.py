import json
import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

FLASK_API_URL = "http://localhost:5000/run_flow"  # URL of the Flask API

def run_flow(message: str) -> dict:
    payload = {
        "input_value": message,
    }
    try:
        response = requests.post(FLASK_API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return {}

def main():
    st.title("Code Generation Interface")

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)

            if 'error' in response:
                st.error(response['error'])
            else:
                code = response.get("code", "No code generated")
                description = response.get("description", "No description available")
                filename = response.get("filename", "no_filename")
                
                st.markdown(f"**Filename**: {filename}")
                st.code(code, language="python")
                st.markdown(f"**Description**: {description}")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
