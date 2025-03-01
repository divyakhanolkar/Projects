# Agentic AI Blog Generation Workflow with LangChain, LangGraph, and Streamlit

## Overview

This project implements an AI-powered **Blog Generation Workflow** that integrates various tools such as **LangChain**, **LangGraph**, and **Streamlit**. The goal is to generate blog posts automatically by first searching the web, summarizing the content, and then using an AI model to write a detailed blog based on that summary. Additionally, a human-in-the-loop feedback mechanism is integrated to refine the blog post based on user input.

## Approach

The project breaks down the blog generation process into **multiple independent steps**, with each step focusing on a specific task. The steps are organized into a **LangGraph workflow** to define a clear flow of data through each stage of the process. Below is a detailed explanation of how each component works.

### 1. Modularization of Tasks

The task is broken down into the following key steps (or nodes in LangGraph):
   - **Search Web**: This step searches the web for relevant information based on a topic provided by the user.
   - **Summarize Results**: The search results are summarized into concise content to be used in the blog post.
   - **Generate Blog**: Using the summarized content, an AI model is employed to generate a blog post on the topic.
   - **Review Blog**: The generated blog is checked to ensure it meets the desired length.
   - **Collect Feedback**: The user is asked for feedback on the generated blog, allowing for improvements and refinements.

These functions are separate and easy to modify or replace without affecting the rest of the workflow.

### 2. LangGraph Workflow

LangGraph is used to organize the tasks into a **Directed Acyclic Graph (DAG)**. The steps are organized as nodes, and the transitions between them are defined by edges. The flow is as follows:
   - **Entry Point**: The process starts at the **search_web** function.
   - **Edges**: Data flows from one node to the next as the process advances through the steps (i.e., `search_web` → `summarize_results` → `generate_blog` → `review_blog` → `collect_feedback`).
   - **End Point**: The process ends when the blog is reviewed and refined based on feedback..

This structure allows you to easily add new steps or modify existing ones. For example, you could add a **plagiarism check** or **grammar check** step without rewriting the entire flow.

### 3. State Management

Each step in the process modifies the **state**, which is a dictionary that holds all the relevant data. The state is passed from one function to the next, preserving the information generated so far:
   - After searching the web, the search results are added to the state.
   - After summarizing the results, the summary is added to the state.
   - After generating the blog, the final blog content is stored in the state.
   - Finally, after receiving user feedback, the blog is refined based on the input.

State is managed by merging data at each step, ensuring that the context is carried forward throughout the process.

### 4. Human-in-the-Loop Feedback Mechanism

A key addition to the workflow is the **human-in-the-loop** feedback mechanism, where users can review the generated blog and provide suggestions for improvement. The workflow includes a collect_feedback step where:
   - The user reviews the generated blog and provides feedback through the Streamlit interface.
   - If the feedback suggests improvements, the AI refines the blog accordingly.
   - If no feedback is provided, the original blog is retained as the final output.

### 5. Use of External APIs
Several external tools and APIs are used in the workflow:
   - **Tavily API**: Used to perform web searches based on the user's input topic.
   - **ChatGroq (Qwen 2.5)**: A custom LLM (Large Language Model) that generates the blog post based on the summarized content.
   - **FAISS**: Used to manage vector stores and handle text-based data efficiently (though it's not fully integrated in this context).
   - **Streamlit**: Provides the user interface where users can input a topic and generate the blog post.

### 5. Environment Variables

Sensitive data, such as the **API keys**, are managed securely using environment variables. This ensures that keys are not hardcoded in the script, keeping them secure.

### 6. LangSmith Debugging

The functions are decorated with `@traceable` from **LangSmith**, which allows for detailed logging and debugging of the process. This helps track the data flow and inspect intermediate outputs, making the development and debugging process easier.

### 7. User Interface with Streamlit

Streamlit is used as a POC to create an interactive web application for users. The UI allows users to input a topic, trigger the blog generation process, and view the final blog post.

## Workflow

The following is the high-level flow of how the process works:
1. **User Input**: The user enters a blog topic.
2. **Search Web**: The `search_web` function queries the web for relevant information based on the user's topic.
3. **Summarize Results**: The `summarize_results` function processes the search results and creates a summary.
4. **Generate Blog**: The `generate_blog` function generates a full blog post based on the summary.
5. **Review Blog**: The `review_blog` function checks the quality of the blog before presenting it to the user.
6. **Collect Feedback**: The user reviews the blog and provides feedback for improvements.
7. **Refine Blog**: The LLM refines the blog based on feedback (if any).
8. **Display Final Blog**: The final version of the blog is displayed on the Streamlit interface.

## Getting Started

To run this project locally:


1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```bash
   cd path/to/1-BlogGeneration
   ```

3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables in a `.env` file:
   ```ini
   LANGCHAIN_TRACING_V2=true
   GROQ_API_KEY=<your_groq_api_key>
   TAVILY_API_KEY=<your_tavily_api_key>
   LANGCHAIN_API_KEY=<your_langchain_api_key>
   ```

6. Run the Streamlit app:
   ```bash
   streamlit run app.py
