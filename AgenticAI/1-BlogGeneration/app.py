import os
import faiss
import streamlit as st
from langchain_groq import ChatGroq
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langgraph.graph import StateGraph, END
from langsmith import traceable

import os
from dotenv import load_dotenv
load_dotenv()

# 🟢 Set up API Keys (Ensure environment variables are correctly set)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# 🟢 Initialize Open-Source LLM (Qwen 2.5 via Groq)
llm = ChatGroq(model="qwen-2.5-32b", temperature=0.7)

# 🟢 Initialize Web Search Tool (Tavily)
web_search_tool = TavilySearchResults(max_results=3)

# 🟢 Initialize FAISS Vector DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
dimension = 384  # Adjust based on embedding model output size
index = faiss.IndexFlatL2(dimension)

vector_store = FAISS(
    embedding_function=embedding_model,
    index=index,
    docstore=InMemoryDocstore({}),
    index_to_docstore_id=InMemoryStore()
)

# 🟠 Define Graph Nodes
@traceable  # LangSmith debugging
def search_web(state):
    """Searches the web for relevant articles using Tavily."""
    query = state["topic"]
    print(f"🔍 Searching web for: {query}")

    search_results = web_search_tool.run(query) or []

    return {**state, "search_results": search_results}  # ✅ Merge state to preserve "topic"


@traceable  # LangSmith debugging
def summarize_results(state):
    """Summarizes the web search results."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Convert search results into Document objects
    documents = [
        Document(page_content=result.get("content", ""), metadata={"source": result.get("url", "")})
        for result in state["search_results"] if result.get("content")
    ]

    if not documents:
        summary = "No relevant information available."
    else:
        splits = text_splitter.split_documents(documents)
        summary = "\n".join(doc.page_content for doc in splits[:3])  # Taking first 3 chunks

    return {**state, "summary": summary}  # ✅ Merge state to preserve "topic"


@traceable  # LangSmith debugging
def generate_blog(state):
    """Generates a blog post based on summarized content."""
    if "summary" not in state:
        raise ValueError("Summary not found in state!")

    prompt = f"""
    Write a detailed blog post on "{state['topic']}" using the information below:

    {state['summary']}
    
    The blog should be engaging, informative, and structured with headings and subheadings.
    """

    response = llm.invoke(prompt)

    return {**state, "blog": response if isinstance(response, str) else response.content}  # ✅ Merge state


@traceable  # LangSmith debugging
def review_blog(state):
    """Performs a final review before publishing."""
    blog = state["blog"]

    if len(blog) < 500:
        raise ValueError("Generated blog is too short! Re-run the process.")

    return {**state, "final_blog": blog}  # ✅ Merge state


# 🟠 Define Human Feedback Node
@traceable  # LangSmith debugging
def collect_feedback(state):
    """Collects feedback from the human user on the generated blog."""
    feedback = state.get("feedback", None)

    if not feedback:
        return {**state, "final_blog": state["final_blog"]}  # No feedback, keep the blog as is

    # Optionally process feedback to improve blog (e.g., re-generate sections)
    if "improve" in feedback.lower():
        new_blog = llm.invoke(f"Refine the following blog with the following feedback: {feedback}:\n\n{state['final_blog']}")
        return {**state, "final_blog": new_blog if isinstance(new_blog, str) else new_blog.content}

    return {**state, "final_blog": state["final_blog"]}  # Return original if no feedback for improvement


# 🟠 Modify LangGraph Workflow to include Human Feedback Node
workflow = StateGraph(dict)
workflow.add_node("search_web", search_web)
workflow.add_node("summarize_results", summarize_results)
workflow.add_node("generate_blog", generate_blog)
workflow.add_node("review_blog", review_blog)
workflow.add_node("collect_feedback", collect_feedback)

# Define edges
workflow.set_entry_point("search_web")
workflow.add_edge("search_web", "summarize_results")
workflow.add_edge("summarize_results", "generate_blog")
workflow.add_edge("generate_blog", "review_blog")
workflow.add_edge("review_blog", "collect_feedback")  # Add feedback after review
workflow.add_edge("collect_feedback", END)  # End the loop after feedback collection

# Compile graph
app = workflow.compile()

# 🟠 Streamlit UI for Feedback
st.set_page_config(page_title="AI Blog Generator with Feedback Loop", page_icon="📝")
st.title("📝 AI Blog Generator with LangGraph, Streamlit & Human Feedback Loop")

# User input
topic = st.text_input("Enter a blog topic:", "")

if topic:
    with st.spinner("Generating your blog... ⏳"):
        result = app.invoke({"topic": topic})
        st.success("✅ Blog Generated!")
        st.subheader("📌 Generated Blog:")
        st.write(result["final_blog"])

    # Collect human feedback
    feedback = st.text_area("Provide feedback on the blog (optional):", "")

    if feedback:
        with st.spinner("Incorporating your feedback... ⏳"):
            result_with_feedback = app.invoke({"topic": topic, "feedback": feedback, "final_blog": result["final_blog"]})
            st.success("✅ Feedback Incorporated!")
            st.subheader("📌 Updated Blog:")
            st.write(result_with_feedback["final_blog"])
else:
    st.warning("⚠️ Please enter a topic first.")
