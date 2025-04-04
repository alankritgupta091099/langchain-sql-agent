import streamlit as st
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent

# Initialize session state for request count
if "request_count" not in st.session_state:
    st.session_state["request_count"] = 0

# Streamlit UI
st.title("SQL Query Agent with OpenAI")
st.write("This app allows you to ask questions in natural language to query a SQLite database using OpenAI's language model.")
st.image("./uml.jpeg", caption="[Database UML class diagram (w3resource)](https://www.w3resource.com/sql/sql-table.php?id=-1)", use_container_width=True)

st.markdown("_Note: Only two queries are allowed so OpenAI won't make me broke :)_")

st.markdown("### Sample Queries:")
st.markdown("1. Find the total order amount for each customer")
st.markdown("2. Find customers with outstanding amounts above a threshold")
st.markdown("3. Get orders by working area")
st.markdown("4. Find agents handling orders above 2000")

# Fetch OpenAI API Key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Connect to the SQLite database
db = SQLDatabase.from_uri("sqlite:///sql_lite_database.db")

# Choose the OpenAI model
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

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
    if st.session_state["request_count"] < 2:
        st.session_state["request_count"] += 1
        with st.spinner("Processing..."):
            response = agent_executor.invoke(question)
            st.write("### Response:")
            st.write(response)
    else:
        st.error("You have reached the maximum limit of 2 queries.")