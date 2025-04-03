import streamlit as st
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
import os

# Streamlit UI
st.title("SQL Query Agent with OpenAI")

# Get user input for OpenAI API key
openai_api_key = st.secrets["OPENAI_API_KEY"];

# Ensure API key is provided
if openai_api_key:
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Connect to the SQLite database
    db = SQLDatabase.from_uri("sqlite:///sql_lite_database.db")

    # Choose the OpenAI model
    llm = OpenAI(
        temperature=0, 
        openai_api_key=openai_api_key
    )

    # Setup agent
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    # User input for SQL query
    question = st.text_area("Ask a question about the database:")

    if st.button("Submit Query"):
        with st.spinner("Processing..."):
            response = agent_executor.invoke(question)
            st.write("### Response:")
            st.write(response)
else:
    st.warning("Please enter your OpenAI API key to proceed.")

