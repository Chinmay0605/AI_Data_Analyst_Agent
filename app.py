from agents.validation import validate_data
from agents.cleaning import clean_data
from agents.visualization import generate_visualizations
import streamlit as st
import pandas as pd
from agents.visualization import generate_visualizations
from agents.insight import InsightAgent
from agents.forecasting import ForecastingAgent
from agents.eda import EDAAgent
from agents.report import ReportAgent

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="🤖",
    layout="wide"
)

# ------------------ SESSION STATE ------------------
if "df" not in st.session_state:
    st.session_state.df = None

# ------------------ SIDEBAR ------------------
st.sidebar.title("🤖 AI Data Analyst Agent")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Dataset",
        "Data Validation",
        "Data Cleaning",
        "EDA",
        "Visualization",
        "AI Insights",
        "Forecasting",
        "Generate Report"
    ]
)

# ------------------ TITLE ------------------
st.title("🤖 AI Data Analyst Agent")
st.write("Analyze your data with Artificial Intelligence.")

# =====================================================
# UPLOAD DATASET
# =====================================================

if menu == "Upload Dataset":

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state.df = df

        st.success("Dataset Uploaded Successfully!")

        st.subheader("Dataset Preview")

        st.dataframe(df)

# =====================================================
# DASHBOARD
# =====================================================

elif menu == "Dashboard":

    if st.session_state.df is not None:

        df = st.session_state.df

        rows = df.shape[0]
        cols = df.shape[1]
        missing = df.isnull().sum().sum()
        duplicate = df.duplicated().sum()

    else:
        rows = cols = missing = duplicate = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", rows)
    col2.metric("Columns", cols)
    col3.metric("Missing Values", missing)
    col4.metric("Duplicate Rows", duplicate)

    st.divider()

    if st.session_state.df is None:
        st.info("Please upload a dataset from the sidebar.")
    else:
        st.success("Dataset Loaded Successfully!")

# =====================================================
# DATA VALIDATION
# =====================================================

elif menu == "Data Validation":

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:

        report = validate_data(st.session_state.df)

        st.header("📋 Data Validation Report")

        c1, c2, c3 = st.columns(3)

        c1.metric("Rows", report["rows"])
        c2.metric("Columns", report["columns"])
        c3.metric("Quality Score", f'{report["quality_score"]}/100')

        st.divider()

        st.subheader("Missing Values")

        st.dataframe(report["missing_by_column"])

        st.subheader("Data Types")

        st.dataframe(report["data_types"])

        st.subheader("Summary")

        st.write(f"✅ Missing Values : {report['missing_values']}")
        st.write(f"✅ Duplicate Rows : {report['duplicate_rows']}")
        st.write(f"✅ Empty Columns : {len(report['empty_columns'])}")
        st.write(f"✅ Constant Columns : {len(report['constant_columns'])}")

        if report["quality_score"] > 90:
            st.success("Excellent Dataset Quality")

        elif report["quality_score"] > 70:
            st.warning("Dataset Quality is Good")

        else:
            st.error("Dataset Needs Cleaning")

# =====================================================
# DATA CLEANING
# =====================================================

elif menu == "Data Cleaning":

    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")

    else:

        st.header("🧹 Data Cleaning")

        if st.button("Clean Dataset"):

            cleaned_df, report = clean_data(st.session_state.df)

            st.session_state.df = cleaned_df

            st.success("Dataset Cleaned Successfully!")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Duplicates Removed",
                report["duplicates_removed"]
            )

            c2.metric(
                "Missing Values Filled",
                report["missing_values_filled"]
            )

            c3.metric(
                "Empty Columns Removed",
                report["empty_columns_removed"]
            )

            st.divider()

            st.subheader("Cleaned Dataset")

            st.dataframe(cleaned_df)

            csv = cleaned_df.to_csv(index=False)

            st.download_button(
                "⬇ Download Cleaned CSV",
                csv,
                "cleaned_dataset.csv",
                "text/csv"
            )

# =====================================================
# VISUALIZATION
# =====================================================

elif menu == "Visualization":

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:
        st.header("📊 Data Visualization")

        charts = generate_visualizations(st.session_state.df)

        st.write("Total Charts Generated:", len(charts))

        for c in charts:
            st.write(c["title"])

        if len(charts) == 0:
            st.warning("No charts can be generated.")
        else:
            for chart in charts:
                st.subheader(chart["title"])
                st.plotly_chart(
                    chart["figure"],
                    use_container_width=True
                )

# ==========================================================
# AI INSIGHTS
# ==========================================================

elif menu == "AI Insights":

    st.title("🤖 AI Insights")

    if "df" not in st.session_state:
        st.warning("Please upload dataset first.")

    else:
        agent = InsightAgent(st.session_state["df"])

        try:
            insights = agent.generate()

            st.session_state["insights"] = insights

            for item in insights:
                st.success(item)

        except Exception as e:
            st.error(e)

# ==========================================================
# FORECASTING
# ==========================================================

elif menu == "Forecasting":

    st.title("📈 Forecasting")

    if "df" not in st.session_state:

        st.warning("Please upload a dataset first.")

    else:

        agent = ForecastingAgent(st.session_state.df)

        # Check whether date columns exist
        if len(agent.date_columns) == 0:

            st.error("❌ No Date Column Found.")

        # Check whether numeric columns exist
        elif len(agent.numeric_columns) == 0:

            st.error("❌ No Numeric Column Found.")

        else:

            date_col = st.selectbox(
                "Select Date Column",
                agent.date_columns
            )

            value_col = st.selectbox(
                "Select Value Column",
                agent.numeric_columns
            )

            periods = st.slider(
                "Forecast Days",
                min_value=7,
                max_value=365,
                value=30
            )

            if st.button("Generate Forecast"):

                fig, forecast = agent.forecast(
                    date_col,
                    value_col,
                    periods
                )

                # Save forecast for Report Agent
                st.session_state["forecast"] = forecast

                st.success("Forecast Generated Successfully!")

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader("Forecast Data")

                st.dataframe(
                    forecast,
                    use_container_width=True
                )

# ====================================================
# EDA
# ====================================================

elif menu == "EDA":

    st.title("📊 Exploratory Data Analysis")

    if "df" not in st.session_state:

        st.warning("Please upload a dataset first.")

    else:

        agent = EDAAgent(st.session_state.df)

        st.header("Dataset Overview")

        overview = agent.overview()

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Rows", overview["Rows"])
        c2.metric("Columns", overview["Columns"])
        c3.metric("Memory (MB)", overview["Memory (MB)"])
        c4.metric("Numeric", overview["Numeric Columns"])
        c5.metric("Categorical", overview["Categorical Columns"])

        st.divider()

        st.subheader("Statistical Summary")

        st.dataframe(agent.statistics(), use_container_width=True)

        st.divider()

        st.subheader("Data Types")

        st.dataframe(agent.data_types(), use_container_width=True)

        st.divider()

        st.subheader("Missing Values")

        st.dataframe(agent.missing_values(), use_container_width=True)

        st.divider()

        st.metric("Duplicate Rows", agent.duplicates())

# ==========================================================
# GENERATE REPORT
# ==========================================================
elif menu == "Generate Report":

    st.title("📄 Generate Report")

    if "df" not in st.session_state:
        st.warning("Upload a dataset first.")

    else:

        if st.button("Generate PDF"):

            # -----------------------------
            # Generate Insights automatically
            # -----------------------------
            if st.session_state.get("insights") is None:

                insight_agent = InsightAgent(st.session_state.df)
                st.session_state["insights"] = insight_agent.generate()

            # -----------------------------
            # Generate Forecast automatically
            # -----------------------------
            if st.session_state.get("forecast") is None:

                try:
                    forecast_agent = ForecastAgent(st.session_state.df)
                    st.session_state["forecast"] = forecast_agent.generate()

                except Exception:
                    st.session_state["forecast"] = None

            # -----------------------------
            # Generate PDF
            # -----------------------------
            report = ReportAgent()

            filename = report.generate(

                df=st.session_state.df,

                validation=st.session_state.get("validation"),

                insights=st.session_state.get("insights"),

                forecast=st.session_state.get("forecast")
            )

            st.success("Report Generated Successfully!")

            with open(filename, "rb") as f:

                st.download_button(
                    label="Download Report",
                    data=f,
                    file_name="Analysis_Report.pdf",
                    mime="application/pdf"
                )