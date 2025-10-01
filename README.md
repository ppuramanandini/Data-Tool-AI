# AI-Data-Tool

[![License](https://img.shields.io/github/license/Kasa-Harendra/AI-Data-Tool?color=blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B)](https://streamlit.io/)

## Description

The AI-Data-Tool is an interactive Streamlit application designed to empower users to analyze and query their tabular data (CSV and Excel files) using natural language. It leverages the power of Large Language Models (LLMs) through [LangChain](https://www.langchain.com/) agents to provide a conversational interface for data exploration. Users can upload their datasets, ask questions about them in plain English, and receive insights, summaries, or even specific data points, making data analysis and processing accessible without writing a single line of code.

**Live App**: [https://ai-data-tool.streamlit.app/](https://ai-data-tool.streamlit.app/)

## Features

*   **Interactive Data Upload**: Easily upload CSV (`.csv`) and Excel (`.xlsx`) files directly within the Streamlit interface.
*   **AI-Powered Data Agent**: Utilizes a [LangChain](https://www.langchain.com/) `PandasAgent` (Implemented on own) to intelligently process natural language queries and interact with the uploaded data.
*   **Conversational Interface**: Engage with your data through a user-friendly chat interface, asking questions and receiving AI-generated responses.
*   **Transparent Code Execution**: When the agent executes Python code (e.g., using Pandas) to answer a question, the generated code can be displayed for transparency.
*   **Preprocess data**: The data can be processed within the chat and can be downloaded. 
*   **Clear Chat History**: Option to clear the current conversation and start fresh with new queries or data.



## Usage

1. **Live App**: [https://ai-data-tool.streamlit.app/](https://ai-data-tool.streamlit.app/)

2.  **Upload Your Data**:
    *   On the left sidebar, use the file uploader to select a `.csv` or `.xlsx` file from your local machine.
    *   Once uploaded, the application will display basic information about the file.

3.  **Chat with Your Data**:
    *   Navigate to the "Chat" page (if not automatically redirected after upload).
    *   In the chat input box at the bottom, type your questions about the uploaded data.
        *   **Example questions:**
            *   "Show me the first 5 rows."
            *   "What are the column names?"
            *   "How many unique values are there in the 'Category' column?"
            *   "Calculate the average of the 'Sales' column."
            *   "Which 'Product' has the highest 'Quantity'?"
            *   "Show me a histogram of the 'Price' column."
    *   Press Enter, and the AI agent will process your query and provide a response.
    *   You can clear the chat history at any time using the "Clear Chat" button in the sidebar.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution Guidelines

We welcome contributions to the AI-Data-Tool! If you're interested in improving the project, please follow these guidelines:

1.  **Fork the repository**: Start by forking the `AI-Data-Tool` repository to your GitHub account.
2.  **Create a new branch**: For each new feature or bug fix, create a dedicated branch.
    ```bash
    git checkout -b feature/your-feature-name
    ```
    or
    ```bash
    git checkout -b bugfix/issue-description
    ```
3.  **Make your changes**: Implement your features or bug fixes.
4.  **Write clear commit messages**: Describe your changes concisely and clearly.
5.  **Test your changes**: Ensure that your modifications do not introduce new bugs and work as expected.
6.  **Submit a Pull Request**: Push your branch to your forked repository and open a pull request against the `main` branch of the original repository. Please provide a detailed description of your changes.

### Ideas for Contribution

*   Add support for more data formats (e.g., JSON, Parquet).
*   Implement more sophisticated data visualization tools.
*   Integrate with different LLM providers (e.g., Google Gemini, Hugging Face models).
*   Improve error handling and user feedback.
*   Enhance security measures, especially around code execution.

## Project Structure

```
PandasAI/
├── .streamlit/
│   └── config.toml         # Streamlit configuration (optional)
├── data/                   # Directory for temporary session data (CSVs, images)
├── pages/
│   └── chat.py             # Streamlit page for the chat interface
├── screenshots/
│   └── UI-*.png            # Screenshots for the README
├── .env                    # Environment variables (e.g., API keys)
├── agent.py                # Core PandasAgent class for AI logic
├── app.py                  # Main Streamlit application entry point
├── README.md               # Project documentation
├── requirements.txt        # Python package dependencies
└── utils.py                # Utility functions (e.g., file uploading)
```

## Screenshots/Examples

1.  **Upload Page**: The main page where users can upload their CSV or Excel files.
    ![Upload Page](./screenshots/UI-1.png)
    ![Data](./screenshots/UI-2.png)

2.  **Chat Interface**: The conversational UI for asking questions about the data.
    ![Chat Interface](./screenshots/UI-3.png)
    ![Chat Interface](./screenshots/UI-4.png)

3.  **Data Visualization**: An example of a plot generated by the AI agent.
    ![Data Visualization](./screenshots/UI-5.png)
    ![Data Visualization](./screenshots/UI-6.png)


**Example Interaction Flow:**

1.  **Upload `sales_data.csv`:**
    ```
    # (Sidebar shows file uploaded)
    ```
2.  **User Query:** "Show me the average sales per region."
    **AI Response:**
    ```
    The average sales per region are:
    Region A    15000.50
    Region B    22000.75
    Region C    18500.20
    Name: Sales, dtype: float64
    ```
3.  **User Query:** "What are the top 3 products by total sales?"
    **AI Response:**
    ```python
    df.groupby('Product')['Sales'].sum().nlargest(3)
    ```
    ```
    Product A    50000
    Product C    35000
    Product B    20000
    Name: Sales, dtype: int64
    ```