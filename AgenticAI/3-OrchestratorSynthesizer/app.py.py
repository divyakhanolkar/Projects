import os
import requests
import streamlit as st
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langsmith import traceable
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🟢 Set up API Keys
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# 🟢 Initialize Open-Source LLM
llm = ChatGroq(model="qwen-2.5-32b", temperature=0.7)

# 🟠 Define Graph Nodes

@traceable  # LangSmith debugging
def fetch_data(state):
    """Fetches data from user-specified sources (URLs or pasted data)."""
    sources = state.get("sources", [])
    fetched_data = []

    for source in sources:
        if source.startswith("http"):  # Check if the source is a URL
            try:
                response = requests.get(source)
                if response.status_code == 200:
                    fetched_data.append(f"Data from {source}: {response.text[:500]}...")  # Truncate for simplicity
                else:
                    fetched_data.append(f"Failed to fetch data from {source}. Status code: {response.status_code}")
            except Exception as e:
                fetched_data.append(f"Error fetching data from {source}: {str(e)}")
        else:  # Assume the source is pasted data
            fetched_data.append(f"Pasted Data: {source}")

    state["fetched_data"] = fetched_data
    return state

@traceable  # LangSmith debugging
def process_data(state):
    """Processes the fetched data."""
    fetched_data = state["fetched_data"]

    # Combine the fetched data into a single string
    processed_data = "Processed Data:\n" + "\n".join(fetched_data)
    state["processed_data"] = processed_data
    return state

@traceable  # LangSmith debugging
def synthesize_report(state):
    """Synthesizes a report based on the processed data."""
    processed_data = state["processed_data"]

    prompt = f"""
    Generate a synthesized report based on the following processed data:
    
    {processed_data}
    
    The report should include:
    - A summary of the key points.
    - Insights or conclusions drawn from the data.
    """
    report = llm.invoke(prompt)
    state["report"] = report.content
    return state

@traceable  # LangSmith debugging
def finalize_output(state):
    """Finalizes the output by ensuring proper formatting."""
    report = state["report"]

    # Check if the report is properly formatted
    if "Summary" not in report or "Insights" not in report:
        # Reformat the report if necessary
        prompt = f"""
        The following report is not properly formatted. Please reformat it to include:
        - Summary
        - Insights

        Report:
        {report}
        """
        formatted_report = llm.invoke(prompt)
        report = formatted_report.content

    state["final_output"] = report
    return state

@traceable  # LangSmith debugging
def collect_feedback(state):
    """Collects feedback from the user on the final output."""
    feedback = state.get("feedback", None)
    if not feedback:
        return state  # No feedback, keep the output as is

    # Optionally process feedback to improve the output
    if "improve" in feedback.lower():
        new_output = llm.invoke(f"Refine the following output with the following feedback: {feedback}:\n\n{state['final_output']}")
        state["final_output"] = new_output.content

    return state

# 🟠 Define LangGraph Workflow
workflow = StateGraph(dict)
workflow.add_node("fetch_data", fetch_data)
workflow.add_node("process_data", process_data)
workflow.add_node("synthesize_report", synthesize_report)
workflow.add_node("finalize_output", finalize_output)
workflow.add_node("collect_feedback", collect_feedback)

# Define edges
workflow.set_entry_point("fetch_data")
workflow.add_edge("fetch_data", "process_data")
workflow.add_edge("process_data", "synthesize_report")
workflow.add_edge("synthesize_report", "finalize_output")
workflow.add_edge("finalize_output", "collect_feedback")
workflow.add_edge("collect_feedback", END)  # End the loop after feedback collection

# Compile graph
app = workflow.compile()

# 🟠 Streamlit UI for Feedback
st.set_page_config(page_title="Orchestrator & Synthesizer Workflow", page_icon="🤖")
st.title("🤖 Orchestrator & Synthesizer Workflow with LangGraph & Streamlit")

# User input for sources
st.subheader("Enter URLs or Paste Data")
custom_inputs = st.text_area(
    "Enter multiple custom inputs (URLs or pasted data, one per line):",
    height=150,
    placeholder="Example:\nhttps://api.example.com/stock-data\nIndia's GDP grew by 6.1% in Q3 2023."
)

# Automatically trigger the workflow when inputs are provided
if custom_inputs.strip():
    sources = custom_inputs.strip().split("\n")
    with st.spinner("Analyzing data and generating a report... ⏳"):
        result = app.invoke({"sources": sources})
        st.success("✅ Report Generated!")
        st.subheader("📌 Generated Report:")
        st.write(result["final_output"])

    # Collect human feedback
    feedback = st.text_area("Provide feedback on the report (optional):", "")

    if feedback:
        with st.spinner("Incorporating your feedback... ⏳"):
            result_with_feedback = app.invoke({"sources": sources, "feedback": feedback, "final_output": result["final_output"]})
            st.success("✅ Feedback Incorporated!")
            st.subheader("📌 Updated Report:")
            st.write(result_with_feedback["final_output"])
else:
    st.warning("⚠️ Please enter URLs or paste data to generate a report.")