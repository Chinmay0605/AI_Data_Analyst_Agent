import pandas as pd

def validate_data(df):
    """
    Validate dataset and return a report dictionary.
    """

    report = {}

    # Basic Information
    report["rows"] = df.shape[0]
    report["columns"] = df.shape[1]

    # Missing Values
    report["missing_values"] = df.isnull().sum().sum()

    # Duplicate Rows
    report["duplicate_rows"] = df.duplicated().sum()

    # Data Types
    report["data_types"] = df.dtypes

    # Missing values by column
    report["missing_by_column"] = df.isnull().sum()

    # Empty Columns
    empty_columns = df.columns[df.isnull().all()].tolist()
    report["empty_columns"] = empty_columns

    # Constant Columns
    constant_columns = []

    for column in df.columns:
        if df[column].nunique() == 1:
            constant_columns.append(column)

    report["constant_columns"] = constant_columns

    # Quality Score
    score = 100

    score -= min(report["missing_values"], 30)
    score -= min(report["duplicate_rows"], 20)
    score -= len(empty_columns) * 10
    score -= len(constant_columns) * 5

    score = max(score, 0)

    report["quality_score"] = score

    return report