import os
import streamlit as st
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langsmith import traceable
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🟢 Set up API Keys (Ensure environment variables are correctly set)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# 🟢 Initialize Open-Source LLM (Qwen 2.5 via Groq)
llm = ChatGroq(model="qwen-2.5-coder-32b", temperature=0.7)

# 🟠 Define Graph Nodes
@traceable  # LangSmith debugging
def collect_code(state):
    """Collects code input from the user."""
    code = state.get("code", None)
    if not code:
        raise ValueError("No code provided!")
    return {**state, "code": code}

@traceable  # LangSmith debugging
def analyze_code(state):
    """Analyzes the code for potential issues, style violations, and best practices."""
    code = state["code"]
    prompt = f"""
    Analyze the following code for potential issues, style violations, and best practices:
    
    {code}
    
    Provide a detailed analysis.
    """
    analysis = llm.invoke(prompt)
    return {**state, "analysis": analysis.content}

@traceable  # LangSmith debugging
def generate_review(state):
    """Generates a peer review report based on the analysis."""
    analysis = state["analysis"]
    prompt = f"""
    Generate a peer review report based on the following analysis:
    
    {analysis}
    
    The review should be structured with clear sections for strengths, weaknesses, and suggestions for improvement.
    Do not include any placeholders like [Author Name], [Your Name], [Date], or [Version/Commit Hash].
    Focus only on the content of the review.
    """
    review = llm.invoke(prompt)
    return {**state, "review": review.content}

@traceable  # LangSmith debugging
def finalize_review(state):
    """Finalizes the review and prepares it for display."""
    review = state["review"]
    return {**state, "final_review": review}

@traceable  # LangSmith debugging
def collect_feedback(state):
    """Collects feedback from the user on the generated review."""
    feedback = state.get("feedback", None)
    if not feedback:
        return {**state, "final_review": state["final_review"]}  # No feedback, keep the review as is

    # Optionally process feedback to improve the review
    if "improve" in feedback.lower():
        new_review = llm.invoke(f"Refine the following review with the following feedback: {feedback}:\n\n{state['final_review']}")
        return {**state, "final_review": new_review.content}

    return {**state, "final_review": state["final_review"]}  # Return original if no feedback for improvement

# 🟠 Define LangGraph Workflow
workflow = StateGraph(dict)
workflow.add_node("collect_code", collect_code)
workflow.add_node("analyze_code", analyze_code)
workflow.add_node("generate_review", generate_review)
workflow.add_node("finalize_review", finalize_review)
workflow.add_node("collect_feedback", collect_feedback)

# Define edges
workflow.set_entry_point("collect_code")
workflow.add_edge("collect_code", "analyze_code")
workflow.add_edge("analyze_code", "generate_review")
workflow.add_edge("generate_review", "finalize_review")
workflow.add_edge("finalize_review", "collect_feedback")  # Add feedback after finalizing
workflow.add_edge("collect_feedback", END)  # End the loop after feedback collection

# Compile graph
app = workflow.compile()

# 🟠 Streamlit UI for Feedback
st.set_page_config(page_title="AI Coding Peer Review with Feedback Loop", page_icon="👨‍💻")
st.title("👨‍💻 AI Coding Peer Review with LangGraph, Streamlit & Human Feedback Loop")

# User input
code = st.text_area("Paste your code below:", height=300)

if code:
    with st.spinner("Analyzing your code and generating a review... ⏳"):
        result = app.invoke({"code": code})
        st.success("✅ Review Generated!")
        st.subheader("📌 Generated Review:")
        st.write(result["final_review"])

    # Collect human feedback
    feedback = st.text_area("Provide feedback on the review (optional):", "")

    if feedback:
        with st.spinner("Incorporating your feedback... ⏳"):
            result_with_feedback = app.invoke({"code": code, "feedback": feedback, "final_review": result["final_review"]})
            st.success("✅ Feedback Incorporated!")
            st.subheader("📌 Updated Review:")
            st.write(result_with_feedback["final_review"])
else:
    st.warning("⚠️ Please paste your code first.")