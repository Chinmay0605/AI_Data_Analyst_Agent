import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

import plotly.express as px


class ForecastingAgent:

    def __init__(self, df):

        self.df = df.copy()

        self.date_columns = []
        self.numeric_columns = []

        self.detect_columns()

    # --------------------------------------------------
    # Detect Date and Numeric Columns
    # --------------------------------------------------

    def detect_columns(self):

        self.numeric_columns = self.df.select_dtypes(
            include="number"
        ).columns.tolist()

        for col in self.df.columns:

            if self.df[col].dtype == "object":

                try:

                    temp = pd.to_datetime(
                        self.df[col],
                        errors="coerce"
                    )

                    if temp.notna().mean() > 0.8:

                        self.df[col] = temp

                        self.date_columns.append(col)

                except:

                    pass

    # --------------------------------------------------
    # Forecast
    # --------------------------------------------------

    def forecast(self, date_col, value_col, periods=30):

        temp = self.df[[date_col, value_col]].dropna()

        temp = temp.sort_values(date_col)

        temp["Day"] = np.arange(len(temp))

        X = temp[["Day"]]

        y = temp[value_col]

        model = LinearRegression()

        model.fit(X, y)

        future_days = np.arange(
            len(temp),
            len(temp) + periods
        )

        future_dates = pd.date_range(

            temp[date_col].max(),

            periods=periods + 1,

            freq="D"

        )[1:]

        predictions = model.predict(

            future_days.reshape(-1, 1)

        )

        forecast_df = pd.DataFrame({

            date_col: future_dates,

            value_col: predictions

        })

        fig = px.line(

            title=f"{value_col} Forecast"

        )

        fig.add_scatter(

            x=temp[date_col],

            y=temp[value_col],

            mode="lines",

            name="Actual"

        )

        fig.add_scatter(

            x=forecast_df[date_col],

            y=forecast_df[value_col],

            mode="lines",

            name="Forecast"

        )

        return fig, forecast_df