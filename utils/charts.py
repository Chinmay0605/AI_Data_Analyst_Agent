import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram(df, column):

    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=f"Distribution of {column}"
    )

    fig.update_layout(template="plotly_white")

    return fig


# ==========================================================
# BOX PLOT
# ==========================================================

def box_plot(df, column):

    fig = px.box(
        df,
        y=column,
        title=f"Box Plot of {column}"
    )

    fig.update_layout(template="plotly_white")

    return fig


# ==========================================================
# SCATTER PLOT
# ==========================================================

def scatter_plot(df, x, y):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=f"{x} vs {y}",
        trendline="ols"
    )

    fig.update_layout(template="plotly_white")

    return fig


# ==========================================================
# BAR CHART
# ==========================================================

def bar_chart(df, category, value):

    grouped = (
        df.groupby(category)[value]
        .sum()
        .reset_index()
    )

    grouped = grouped.sort_values(
        value,
        ascending=False
    )

    fig = px.bar(
        grouped,
        x=category,
        y=value,
        title=f"{value} by {category}"
    )

    fig.update_layout(template="plotly_white")

    return fig


# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(df, category, value):

    grouped = (
        df.groupby(category)[value]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        grouped,
        names=category,
        values=value,
        hole=0.45,
        title=f"{value} Share by {category}"
    )

    fig.update_layout(template="plotly_white")

    return fig


# ==========================================================
# LINE CHART
# ==========================================================

def line_chart(df, x, y):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=f"{y} Trend"
    )

    fig.update_layout(template="plotly_white")

    return fig


# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

def correlation_heatmap(df):

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1
        )
    )

    fig.update_layout(
        title="Correlation Heatmap",
        template="plotly_white"
    )

    return fig

def monthly_sales(df):

    if "Order Date" not in df.columns or "Sales" not in df.columns:
        return None

    temp = df.copy()

    temp["Order Date"] = pd.to_datetime(
        temp["Order Date"],
        errors="coerce"
    )

    temp["Month"] = temp["Order Date"].dt.to_period("M").astype(str)

    grouped = (
        temp.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        grouped,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(template="plotly_white")

    return fig

def monthly_profit(df):

    if "Order Date" not in df.columns or "Profit" not in df.columns:
        return None

    temp = df.copy()

    temp["Order Date"] = pd.to_datetime(
        temp["Order Date"],
        errors="coerce"
    )

    temp["Month"] = temp["Order Date"].dt.to_period("M").astype(str)

    grouped = (
        temp.groupby("Month")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        grouped,
        x="Month",
        y="Profit",
        markers=True,
        title="Monthly Profit Trend"
    )

    fig.update_layout(template="plotly_white")

    return fig

def sales_by_category(df):

    if "Category" not in df.columns:
        return None

    return bar_chart(df, "Category", "Sales")

def profit_by_category(df):

    if "Category" not in df.columns:
        return None

    return bar_chart(df, "Category", "Profit")

    