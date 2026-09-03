import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import re
import json
import matplotlib.pyplot as plt


# Load API key


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found. Please check your .env file.")
    st.stop()

groq_client = Groq(api_key=api_key)


# Page configuration


st.set_page_config(
    page_title="AI Data Analyst Assistant",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.main-title {font-size: 2.2rem; font-weight: 700; margin-bottom: .2rem;}
.subtitle {color: #6b7280; font-size: 1rem; margin-bottom: 1.2rem;}
.section-title {font-size: 1.25rem; font-weight: 650; margin-top: .4rem;}
div[data-testid="stMetric"] {
    padding: .8rem;
    border: 1px solid rgba(128,128,128,.18);
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🧠 DataMate</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">AI-Powered CSV Data Analyst — Upload, Ask, Analyze & Visualize</div>',
    unsafe_allow_html=True
)


# Upload CSV


tab_upload, tab_explore, tab_ask = st.tabs(
    ["📁 Upload", "📊 Explore", "💬 Ask DataMate"]
)

with tab_upload:
    st.markdown(
        '<div class="section-title">Upload your dataset</div>',
        unsafe_allow_html=True
    )
    st.caption("CSV files only. Your dataset stays in this Streamlit session.")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        label_visibility="collapsed"
    )


# Continue only after CSV upload


if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

    except Exception as e:

        st.error(f"Could not read the CSV file: {e}")
        st.stop()

    st.success("CSV uploaded successfully!")


    with tab_explore:
     
        # Dataset Overview
    

        st.subheader("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )


        # Dataset Preview
  

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )


   
        # Column Information
    

        st.subheader("📋 Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(
            column_info,
            use_container_width=True
        )


        # Basic Statistics


        st.subheader("📈 Basic Statistics")

        try:

            st.dataframe(
                df.describe(include="all"),
                use_container_width=True
            )

        except Exception:

            st.info(
                "Statistics could not be generated for this dataset."
            )


    with tab_ask:
   
        # Ask DataMate
    

        st.subheader("💬 Ask DataMate")

        question = st.text_input(
            "What would you like to know?",
            placeholder="Example: Which region has the highest profit?"
        )


        # Process question


        if question.strip():

            dataset_info = f"""
    Dataset shape:
    Rows: {df.shape[0]}
    Columns: {df.shape[1]}

    Columns and data types:
    {column_info.to_string(index=False)}

    Sample data:
    {df.head(5).to_string(index=False)}
    """


            # ONE Groq API request
          

            prompt = f"""
    You are DataMate, an AI Data Analyst.

    The user uploaded a CSV dataset.

    {dataset_info}

    User question:
    {question}

    Your task is to determine how the question should
    be answered using the dataframe `df`.

    Return ONLY valid JSON.

    The JSON must contain exactly these fields:

    {{
        "pandas_expression": "ONE valid Python Pandas expression",
        "needs_chart": true or false,
        "chart_type": "bar" or "line" or "pie" or "histogram" or "none"
    }}

    IMPORTANT RULES:

    1. The dataframe is already available as `df`.
    2. Use ONLY the dataframe `df`.
    3. Use actual column names from the dataset.
    4. Do not load another file.
    5. Do not create fake data.
    6. The Pandas expression must calculate the answer
       from the actual dataset.
    7. If the user asks for highest or lowest,
       perform the required aggregation first.
    8. If the user asks for both a category and its
       numerical value, return both.
    9. If the user asks to show, plot, visualize,
       graph, or chart something, set needs_chart to true.
    10. If the user only asks for a direct answer,
        set needs_chart to false.
    11. Return only JSON.
    12. Do not use markdown.
    13. Do not include explanations outside the JSON.


    Examples:

    Question:
    Which region has the highest profit?

    IMPORTANT:
    When calculating a rate, percentage, or proportion for a binary
    0/1 column, use mean() after grouping rather than max(), min(),
    first(), or mode().

    For Titanic-style survival data:
    df.groupby("Sex")["Survived"].mean()

    If the user asks for "survival rate", "success rate",
    "percentage", or "proportion", calculate the actual rate,
    not the binary label itself.

    Response:
    {{
        "pandas_expression": "df.groupby('Region')['Total Profit'].sum().sort_values(ascending=False).head(1)",
        "needs_chart": false,
        "chart_type": "none"
    }}

    Question:
    Which region has the highest profit and what is the value?

    Response:
    {{
        "pandas_expression": "df.groupby('Region')['Total Profit'].sum().sort_values(ascending=False).head(1)",
        "needs_chart": false,
        "chart_type": "none"
    }}

    Question:
    Show me total profit by region.

    Response:
    {{
        "pandas_expression": "df.groupby('Region')['Total Profit'].sum().sort_values(ascending=False)",
        "needs_chart": true,
        "chart_type": "bar"
    }}

    Question:
    Plot revenue by region.

    Response:
    {{
        "pandas_expression": "df.groupby('Region')['Total Revenue'].sum().sort_values(ascending=False)",
        "needs_chart": true,
        "chart_type": "bar"
    }}

    Question:
    What is the average total revenue?

    Response:
    {{
        "pandas_expression": "df['Total Revenue'].mean()",
        "needs_chart": false,
        "chart_type": "none"
    }}
    """


            # Call Groq
          

            try:

                with st.spinner("DataMate is analyzing your data..."):

                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0
                    )

            except Exception as e:

                error_message = str(e)

                if "429" in error_message:

                    st.warning(
                        "⚠️ Groq API rate limit reached. "
                        "Please wait a little and try again."
                    )

                else:

                    st.error(
                        "Unable to connect to the Groq API."
                    )

                st.stop()


        
            # Get Groq response
           

            response_text = response.choices[0].message.content.strip()


            # Clean JSON response
          

            response_text = re.sub(
                r"```json|```",
                "",
                response_text
            ).strip()


            # Parse JSON
            

            try:

                analysis = json.loads(response_text)

                generated_code = analysis["pandas_expression"]

                needs_chart = analysis["needs_chart"]

                chart_type = analysis["chart_type"]

            except Exception:

                st.error(
                    "DataMate returned an invalid analysis. "
                    "Please try asking the question again."
                )

                st.stop()


            # Execute Pandas analysis
          

            try:

                result = eval(
                    generated_code,
                    {
                        "pd": pd,
                        "__builtins__": {}
                    },
                    {
                        "df": df
                    }
                )

            except Exception:

                st.error(
                    "DataMate couldn't perform this analysis."
                )

                st.info(
                    "Try asking your question in a simpler way."
                )

                st.stop()


            # Helper: explain verified result
            

            def explain_result_with_llm(question, result):
                try:
                    if isinstance(result, pd.DataFrame):
                        result_text = result.to_string(index=False)
                    elif isinstance(result, pd.Series):
                        result_text = result.to_string()
                    else:
                        result_text = str(result)

                    explanation_prompt = f"""
You are DataMate, an AI data analyst.

User question:
{question}

Pandas has ALREADY calculated this verified result:
{result_text}

Explain this result naturally in 2-4 short sentences.

Rules:
- Do not recalculate or change any value.
- Do not invent facts.
- Directly answer the user's question.
- Mention important categories and values when useful.
- If values are rates between 0 and 1, describe them as percentages.
- Do not show Python code.
"""

                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Explain verified data-analysis results. "
                                    "Never alter supplied values."
                                )
                            },
                            {"role": "user", "content": explanation_prompt}
                        ],
                        temperature=0.2,
                        max_tokens=180
                    )
                    return response.choices[0].message.content.strip()
                except Exception:
                    return None


            # Display DataMate result
          

            st.subheader("🤖 DataMate's Analysis")

            explanation = explain_result_with_llm(question, result)

            if explanation:
                st.markdown("### 💬 Answer")
                st.write(explanation)
            else:
                st.info(
                    "The calculated result is shown below. "
                    "A natural-language explanation could not be generated."
                )

        
            st.markdown("### 📊 Calculated Result")

            is_rate_question = any(
                word in question.lower()
                for word in (
                    "rate", "percentage", "percent",
                    "proportion", "share"
                )
            )

            if isinstance(result, pd.DataFrame):

                display_result = result.copy()

                if is_rate_question:
                    for column in display_result.columns:
                        if pd.api.types.is_numeric_dtype(
                            display_result[column]
                        ):
                            values = display_result[column].dropna()

                            if (
                                len(values) > 0
                                and values.between(0, 1).all()
                            ):
                                display_result[column] = (
                                    display_result[column] * 100
                                ).round(2).astype(str) + "%"
                                break

                st.dataframe(
                    display_result,
                    use_container_width=True
                )

            elif isinstance(result, pd.Series):

                result_df = result.reset_index()

                if is_rate_question:
                    value_column = result_df.columns[-1]

                    if pd.api.types.is_numeric_dtype(
                        result_df[value_column]
                    ):
                        values = result_df[value_column].dropna()

                        if (
                            len(values) > 0
                            and values.between(0, 1).all()
                        ):
                            result_df[value_column] = (
                                result_df[value_column] * 100
                            ).round(2).astype(str) + "%"

                st.dataframe(
                    result_df,
                    use_container_width=True
                )

            else:

                if isinstance(result, (int, float)) and not pd.isna(result):

                    if is_rate_question and 0 <= result <= 1:
                        st.metric(
                            "Calculated Rate",
                            f"{result * 100:.2f}%"
                        )
                    else:
                        st.metric(
                            "Calculated Value",
                            f"{result:,.2f}"
                        )
                else:
                    st.write(result)

            
            with st.expander("🧠 How DataMate analyzed it"):
                st.write(
                    "DataMate converted your question into a Pandas "
                    "operation. Pandas calculated the result directly "
                    "from the uploaded CSV. The explanation above was "
                    "generated only from that calculated result."
                )
                st.code(generated_code, language="python")

           
            # Visualization
           

            if needs_chart and chart_type != "none":

                st.subheader("📊 Visualization")

                try:

                    if isinstance(result, pd.Series):

                        if chart_type == "bar":
                            plot_data = result.sort_values()
                            fig, ax = plt.subplots(figsize=(5.5, 3.8))
                            plot_data.plot(kind="barh", ax=ax)
                            ax.set_xlabel(result.name or "Value", fontsize=9)
                            ax.set_ylabel("")
                            ax.tick_params(axis="y", labelsize=7)
                            ax.tick_params(axis="x", labelsize=7)
                            plt.subplots_adjust(left=0.38, right=0.96, top=0.92, bottom=0.18)
                            st.pyplot(fig, width="content")
                            plt.close(fig)

                        elif chart_type == "line":
                            fig, ax = plt.subplots(figsize=(5.5, 3.5))
                            result.plot(kind="line", ax=ax, marker="o")
                            ax.set_xlabel(result.index.name or "", fontsize=9)
                            ax.set_ylabel(result.name or "Value", fontsize=9)
                            ax.tick_params(axis="both", labelsize=7)
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            st.pyplot(fig, width="content")
                            plt.close(fig)

                        elif chart_type == "pie":
                            fig, ax = plt.subplots(figsize=(4.5, 4.0))
                            result.plot(kind="pie", ax=ax, autopct="%1.1f%%", textprops={"fontsize": 7})
                            ax.set_ylabel("")
                            plt.tight_layout()
                            st.pyplot(fig, width="content")
                            plt.close(fig)

                        elif chart_type == "histogram":
                            fig, ax = plt.subplots(figsize=(5.5, 3.5))
                            result.plot(kind="hist", ax=ax)
                            ax.tick_params(axis="both", labelsize=7)
                            plt.tight_layout()
                            st.pyplot(fig, width="content")
                            plt.close(fig)

                    elif isinstance(result, pd.DataFrame):
                        numeric_columns = result.select_dtypes(include="number").columns

                        if len(numeric_columns) > 0:
                            fig, ax = plt.subplots(figsize=(5.5, 3.5))

                            if chart_type == "bar":
                                result[numeric_columns].plot(kind="bar", ax=ax)
                            elif chart_type == "line":
                                result[numeric_columns].plot(kind="line", ax=ax)

                            ax.tick_params(axis="both", labelsize=7)
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            st.pyplot(fig, width="content")
                            plt.close(fig)
                        else:
                            st.info("The result does not contain numeric data suitable for a chart.")

                    else:
                        st.info("This result cannot be visualized.")

                except Exception as e:
                    st.info("DataMate could not create a visualization for this result.")
                    st.caption(f"Visualization details: {e}")
