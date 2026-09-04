# DataMate — AI Data Analyst Assistant

> Ask questions about your CSV data in plain English and get instant, data-driven answers with visualizations.

DataMate is an AI-powered data analysis application built with **Python, Streamlit, Pandas, Groq, and Matplotlib**. It allows users to upload a CSV dataset, ask questions in natural language, and automatically perform the required data analysis.

---

## Features

-  **CSV Upload** — Upload and explore your own datasets
-  **Natural Language Queries** — Ask questions without writing Python code
-  **Pandas Analysis** — Generate and execute data-analysis operations
-  **AI-Powered Answers** — Get easy-to-understand explanations of results
-  **Data Visualization** — Generate charts when required
-  **Analysis Transparency** — View how DataMate analyzed your question
-  **Dataset Explorer** — View dataset structure, columns, data types, and statistics

---

## How It Works

```text
        CSV Dataset
             │
             ▼
      ┌──────────────┐
      │    DataMate  │
      └──────┬───────┘
             │
             ▼
     Natural Language
          Question
             │
             ▼
        Groq AI Model
             │
             ▼
     Pandas Expression
             │
             ▼
     Verified Data Result
             │
        ┌────┴────┐
        ▼         ▼
     Answer    Visualization
```

---

 ## Example Questions

DataMate can answer questions such as:

- Which region has the highest profit?
- What is the average age?
- What is the survival rate by gender?
- Which category has the highest sales?
- Show total revenue by region.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming |
| **Streamlit** | Web application interface |
| **Pandas** | Data analysis |
| **Groq API** | AI-powered query understanding |
| **Matplotlib** | Data visualization |
| **python-dotenv** | Environment variable management |

---    

## Installation

```bash
git clone https://github.com/amirthayani874-gif/DataMate-AI-Data-Analyst.git
cd DataMate-AI-Data-Analyst
pip install -r requirements.txt
```
**Create a .env file and add your Groq API key:**

GROQ_API_KEY=your_groq_api_key

**Run the application:**

streamlit run app.py

---

## Project Goal

The goal of DataMate is to make data analysis accessible to users who may not know how to write Python or Pandas code.

Instead of manually writing queries and analysis code, users can simply ask questions in natural language and let DataMate perform the analysis.

---

## Future Improvements

1. Support for Excel and other file formats
2. More advanced visualizations
3. Export analysis reports
4. Conversational follow-up questions
5. Advanced statistical analysis
6. Cloud deployment

---

## Author

Sathya Varshaa S. T

B.Tech — Artificial Intelligence & Data Science
