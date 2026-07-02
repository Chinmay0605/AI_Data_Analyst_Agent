from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class ReportAgent:

    def __init__(self, filename="Analysis_Report.pdf"):
        self.filename = filename
        self.styles = getSampleStyleSheet()

    def generate(
        self,
        df,
        validation=None,
        insights=None,
        forecast=None
    ):

        doc = SimpleDocTemplate(self.filename)
        elements = []

        # ===========================
        # TITLE
        # ===========================

        elements.append(
            Paragraph(
                "AI Data Analyst Report",
                self.styles["Title"]
            )
        )

        elements.append(Spacer(1, 0.3 * inch))

        # ===========================
        # DATASET SUMMARY
        # ===========================

        elements.append(
            Paragraph(
                "<b>Dataset Summary</b>",
                self.styles["Heading2"]
            )
        )

        summary = [
            ["Metric", "Value"],
            ["Rows", df.shape[0]],
            ["Columns", df.shape[1]],
            ["Missing Values", int(df.isnull().sum().sum())],
            ["Duplicate Rows", int(df.duplicated().sum())]
        ]

        summary_table = Table(summary)

        summary_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ])
        )

        elements.append(summary_table)

        elements.append(Spacer(1, 0.3 * inch))

        # ===========================
        # AI INSIGHTS
        # ===========================

        elements.append(
            Paragraph(
                "<b>AI Insights</b>",
                self.styles["Heading2"]
            )
        )

        if insights:

            for item in insights:
                elements.append(
                    Paragraph(
                        f"• {item}",
                        self.styles["BodyText"]
                    )
                )

        else:

            elements.append(
                Paragraph(
                    "No AI insights available.",
                    self.styles["BodyText"]
                )
            )

        elements.append(Spacer(1, 0.3 * inch))

        # ===========================
        # FORECAST
        # ===========================

        if forecast is not None:

            elements.append(
                Paragraph(
                    "<b>Forecast (Top 10 Rows)</b>",
                    self.styles["Heading2"]
                )
            )

            forecast = forecast.copy()

            for col in forecast.select_dtypes(include=["float"]).columns:
                forecast[col] = forecast[col].round(2)

            data = [forecast.columns.tolist()]
            data += forecast.head(10).values.tolist()

            forecast_table = Table(data)

            forecast_table.setStyle(
                TableStyle([
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ])
            )

            elements.append(forecast_table)

        else:

            elements.append(
                Paragraph(
                    "<b>Forecast:</b> Nothing to forecast.",
                    self.styles["BodyText"]
                )
            )

        # ===========================
        # BUILD PDF
        # ===========================

        doc.build(elements)

        return self.filename