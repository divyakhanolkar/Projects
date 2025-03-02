# Agentic AI Code Review Workflow with LangChain, LangGraph, and Streamlit

## Overview

This project implements an AI-agent for **Code Review Workflow** that integrates various tools such as **LangChain**, **LangGraph**, and **Streamlit**. The goal is to automate the process of peer code reviews by analyzing code, generating a review report, and allowing users to provide feedback for refinement.

## Approach

The project breaks down the code review process into **multiple independent steps**, with each step focusing on a specific task. The steps are organized into a **LangGraph workflow** to define a clear flow of data through each stage of the process. Below is a detailed explanation of how each component works.

### 1. Modularization of Tasks

The task is broken down into the following key steps (or nodes in LangGraph):
   - **Collect Code**: Collects the user's code input.
   - **Analyze Code**: Analyzes the code for potential issues, style violations, and best practices using an AI model.
   - **Generate Review**: Generates a peer review report based on the analysis.
   - **Finalize Review**: Prepares the review for display.
   - **Collect Feedback**: Collects and processes user feedback to refine the review.

These functions are separate and easy to modify or replace without affecting the rest of the workflow.

### 2. LangGraph Workflow

LangGraph is used to organize the tasks into a **Directed Acyclic Graph (DAG)**. The steps are organized as nodes, and the transitions between them are defined by edges. The flow is as follows:
   - **Entry Point**: The process starts at the **collect_code** function.
   - **Edges**: Data flows from one node to the next as the process advances through the steps (i.e., `collect_code` → `analyze_code` → `generate_review` → `finalize_review` → `collect_feedback`).
   - **End Point**: The process ends when the review is finalized and refined based on feedback.


### 3. State Management

Each step in the process modifies the **state**, which is a dictionary that holds all the relevant data. The state is passed from one function to the next, preserving the information generated so far:
   - After collecting the code, the code is added to the state.
   - After analyzing the code, the analysis is added to the state.
   - After generating the review, the review content is stored in the state.
   - Finally, after receiving user feedback, the review is refined based on the input.

State is managed by merging data at each step, ensuring that the context is carried forward throughout the process.

### 4. Human-in-the-Loop Feedback Mechanism

A key addition to the workflow is the **human-in-the-loop** feedback mechanism, where users can review the generated report and provide suggestions for improvement. The workflow includes a `collect_feedback` step where:
   - The user reviews the generated review and provides feedback through the Streamlit interface.
   - If the feedback suggests improvements, the AI agent refines the review accordingly.
   - If no feedback is provided, the original review is retained as the final output.

### 5. Use of External APIs

Several external tools and APIs are used in the workflow:
   - **ChatGroq (Qwen 2.5 Coder 32B)**: A custom LLM (Large Language Model) that analyzes the code and generates the review report.
   - **Streamlit**: Used as a POC to provide the user interface where users can input their code and view the review.

### 6. Environment Variables

Sensitive data, such as the **API keys**, are managed securely using environment variables.

### 7. LangSmith Debugging

The functions are decorated with `@traceable` from **LangSmith**, which allows for detailed logging and debugging of the process. This helps track the data flow and inspect intermediate outputs, making the development and debugging process easier.


## Workflow

The following is the high-level flow of how the process works:
1. **User Input**: The user inputs their code into the Streamlit interface.
2. **Collect Code**: The `collect_code` function collects the code and adds it to the state.
3. **Analyze Code**: The `analyze_code` function analyzes the code for potential issues, style violations, and best practices.
4. **Generate Review**: The `generate_review` function generates a peer review report based on the analysis.
5. **Finalize Review**: The `finalize_review` function prepares the review for display. In the current workflow this function is just acting as a placeholder. However, for future extension, it will be used to perform additional tasks like formatting the review, adding metadata, or performing final checks before displaying the review.
6. **Collect Feedback**: The user reviews the generated review and provides feedback for improvements.
7. **Refine Review**: The LLM refines the review based on feedback (if any).
8. **Display Final Review**: The final version of the review is displayed on the Streamlit interface.

## Getting Started

To run this project locally:

1. Clone the repository:
   ```bash
   git clone <repository_url>

2. Navigate to the project directory:
   ```bash
   cd path/to/2-CodeReview
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
   LANGCHAIN_API_KEY=<your_langchain_api_key>
   ```

6. Run the Streamlit app:
   ```bash
   streamlit run app.py