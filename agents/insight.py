import pandas as pd
import numpy as np


class InsightAgent:

    def __init__(self, df):
        self.df = df

    def generate(self):

        if self.df is None:
            return ["Dataset is None"]

        insights = []

        rows, cols = self.df.shape

        insights.append(f"Dataset contains {rows:,} rows and {cols} columns.")

        # Missing Values
        missing = self.df.isnull().sum().sum()

        if missing == 0:
            insights.append("No missing values found.")
        else:
            insights.append(f"Dataset contains {missing} missing values.")

        # Duplicate Rows
        duplicates = self.df.duplicated().sum()

        if duplicates == 0:
            insights.append("No duplicate rows found.")
        else:
            insights.append(f"{duplicates} duplicate rows detected.")

        # Numeric Columns
        numeric = self.df.select_dtypes(include=np.number)

        if len(numeric.columns):

            for col in numeric.columns:

                insights.append(
                    f"{col}: Mean = {numeric[col].mean():.2f}"
                )

                insights.append(
                    f"{col}: Maximum = {numeric[col].max():.2f}"
                )

                insights.append(
                    f"{col}: Minimum = {numeric[col].min():.2f}"
                )

        # Correlation
        if len(numeric.columns) >= 2:

            corr = numeric.corr()

            corr_values = []

            for i in range(len(corr.columns)):
                for j in range(i + 1, len(corr.columns)):

                    corr_values.append((
                        corr.iloc[i, j],
                        corr.columns[i],
                        corr.columns[j]
                    ))

            if corr_values:

                best = max(corr_values, key=lambda x: abs(x[0]))

                insights.append(
                    f"Highest correlation: {best[1]} and {best[2]} ({best[0]:.2f})"
                )

        # Categorical Columns
        categorical = self.df.select_dtypes(include="object")

        for col in categorical.columns:

            if self.df[col].nunique() <= 20:

                top = self.df[col].value_counts().idxmax()

                insights.append(
                    f"Most frequent {col}: {top}"
                )

        return insights

