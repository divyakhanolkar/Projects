# Orchestrix: AI-Powered Data Orchestrator and Report Synthesizer

This application automates the process of **fetching data from multiple sources**, **processing it**, and **generating a synthesized report** using an AI-powered workflow. It leverages **LangGraph** for defining the workflow, **Streamlit** for the user interface, and the **Groq LLM** (Qwen 2.5) for generating the report. Users can provide **URLs** or **pasted data** as inputs and refine the output through a **feedback loop**.

---

## Use Case

The application is designed for scenarios where users need to:
1. **Aggregate Data**: Fetch data from multiple sources (e.g., URLs, APIs, or pasted text).
2. **Process Data**: Clean, combine, and analyze the fetched data.
3. **Generate Reports**: Create a synthesized report summarizing key insights and conclusions.
4. **Refine Output**: Incorporate user feedback to improve the report.

### Example Use Cases
- **Business Intelligence**: Analyze data from multiple business systems (e.g., sales, marketing, finance) to generate actionable insights.
- **News Aggregation**: Summarize news articles from multiple sources into a cohesive report.
- **Financial Analysis**: Fetch stock market data, economic indicators, and news to generate investment reports.
- **Scientific Research**: Aggregate data from experiments or research papers and synthesize it into a report.

---

## Approach

The application is built using a **modular workflow with state management** defined with **LangGraph**. Below is a breakdown of the approach:

### 1. **Modular Workflow Design**
   - The workflow is divided into **independent nodes**, each responsible for a specific task:
     - **Fetch Data**: Fetches data from URLs or processes pasted data.
     - **Process Data**: Combines and structures the fetched data.
     - **Synthesize Report**: Gnerates a report based on the processed data.
     - **Finalize Output**: Ensures the report is properly formatted.
     - **Collect Feedback**: Allows users to provide feedback and refine the report.
   - Each node is **traceable** using LangSmith for debugging and monitoring.

### 2. **State Management**
   - The workflow maintains a **state dictionary** that is passed between nodes.
   - Each node modifies the state (e.g., adding fetched data, processed data, or the final report).
   - This ensures that the context is preserved throughout the workflow.

### 3. **User Input Handling**
   - Users can provide **URLs** or **pasted data** as inputs.
   - The application automatically triggers the workflow when inputs are provided.

### 4. **Feedback Loop**
   - Users can provide feedback on the generated report.
   - The feedback is used to refine the report, ensuring it meets the user's requirements.

### 5. **Streamlit UI**
   - The user interface is built using **Streamlit**, providing an intuitive way for users to:
     - Enter inputs (URLs or pasted data).
     - View the generated report.
     - Provide feedback and see the updated report.

### 6. **LangSmith Integration**
   - Each step in the workflow is traced using the `@traceable` decorator.
   - This allows for detailed monitoring and debugging of the workflow in **LangSmith**.

---

## Features

1. **Data Fetching**:
   - Fetch data from **URLs** or accept **pasted data**.
   - Handle errors gracefully (e.g., invalid URLs or network issues).

2. **Data Processing**:
   - Combine fetched data into a single, structured format.

3. **Report Generation**:
   - Use an **LLM** to generate a synthesized report with:
     - **Summary**: Key points from the data.
     - **Insights**: Conclusions and actionable insights.

4. **Feedback Loop**:
   - Allow users to provide feedback on the generated report.
   - Refine the report based on user feedback.

5. **Streamlit UI**:
   - Provide an intuitive interface for users to input data, view reports, and provide feedback.

---

# Getting Started

To run this project locally:


1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```bash
   cd path/to/3-OrchestatorSynthesizer
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
