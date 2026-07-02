import pandas as pd

from utils.charts import (
    histogram,
    box_plot,
    scatter_plot,
    bar_chart,
    pie_chart,
    line_chart,
    correlation_heatmap
)


class VisualizationAgent:

    def __init__(self, df):

        self.df = df.copy()

        self.numeric = []
        self.categorical = []
        self.datetime = []

        self.detect_columns()

    # -------------------------------------------------
    # Detect Columns
    # -------------------------------------------------

    def detect_columns(self):

        # Numeric columns
        self.numeric = self.df.select_dtypes(
            include="number"
        ).columns.tolist()

        # Categorical columns
        self.categorical = self.df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        self.datetime = []

        # Convert ONLY object columns to datetime
        for col in self.categorical.copy():

            try:
                converted = pd.to_datetime(
                    self.df[col],
                    errors="raise"
                )

                self.df[col] = converted

                self.datetime.append(col)

                # remove from categorical after conversion
                self.categorical.remove(col)

            except:
                pass

        # Remove unwanted numeric columns
        remove = []

        for col in self.numeric:

            lower = col.lower()

            if "id" in lower:
                remove.append(col)

            elif "postal" in lower:
                remove.append(col)

            elif self.df[col].nunique() <= 1:
                remove.append(col)

        self.numeric = [
            c for c in self.numeric
            if c not in remove
        ]

    # -------------------------------------------------
    # Generate Charts
    # -------------------------------------------------

    def generate(self):

        charts = []

        # -----------------------------------------
        # Histogram
        # -----------------------------------------

        for col in self.numeric:

            try:

                charts.append({

                    "title": f"Distribution of {col}",

                    "figure": histogram(
                        self.df,
                        col
                    )

                })

            except:

                pass

        # -----------------------------------------
        # Box Plot
        # -----------------------------------------

        for col in self.numeric:

            try:

                charts.append({

                    "title": f"Box Plot - {col}",

                    "figure": box_plot(
                        self.df,
                        col
                    )

                })

            except:

                pass

        # -----------------------------------------
        # Scatter Plot
        # -----------------------------------------

        if len(self.numeric) >= 2:

            try:

                charts.append({

                    "title": "Scatter Plot",

                    "figure": scatter_plot(

                        self.df,

                        self.numeric[0],

                        self.numeric[1]

                    )

                })

            except:

                pass

        # -----------------------------------------
        # Heatmap
        # -----------------------------------------

        if len(self.numeric) >= 2:

            try:

                charts.append({

                    "title": "Correlation",

                    "figure": correlation_heatmap(
                        self.df
                    )

                })

            except:

                pass

        # -----------------------------------------
        # Bar Charts
        # -----------------------------------------

        for cat in self.categorical:

            if self.df[cat].nunique() > 15:

                continue

            for num in self.numeric:

                try:

                    charts.append({

                        "title": f"{num} by {cat}",

                        "figure": bar_chart(

                            self.df,

                            cat,

                            num

                        )

                    })

                except:

                    pass

        # -----------------------------------------
        # Pie Charts
        # -----------------------------------------

        for cat in self.categorical:

            if self.df[cat].nunique() > 8:

                continue

            try:

                charts.append({

                    "title": f"{cat} Share",

                    "figure": pie_chart(

                        self.df,

                        cat,

                        self.numeric[0]

                    )

                })

            except:

                pass

        # -----------------------------------------
        # Line Charts
        # -----------------------------------------

        for date in self.datetime:

            for num in self.numeric:

                try:

                    grouped = (

                        self.df

                        .groupby(date)[num]

                        .sum()

                        .reset_index()

                    )

                    charts.append({

                        "title": f"{num} Trend",

                        "figure": line_chart(

                            grouped,

                            date,

                            num

                        )

                    })

                except:

                    pass

        return charts

def generate_visualizations(df):

    agent = VisualizationAgent(df)

    return agent.generate()