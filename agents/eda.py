import pandas as pd
import numpy as np


class EDAAgent:

    def __init__(self, df):

        self.df = df.copy()

        self.numeric = self.df.select_dtypes(include=np.number)

        self.categorical = self.df.select_dtypes(include="object")


    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    def overview(self):

        memory = self.df.memory_usage(deep=True).sum() / 1024 / 1024

        return {

            "Rows": self.df.shape[0],

            "Columns": self.df.shape[1],

            "Memory (MB)": round(memory,2),

            "Numeric Columns": len(self.numeric.columns),

            "Categorical Columns": len(self.categorical.columns)

        }


    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        return self.df.describe(include="all").fillna("")


    # =====================================================
    # DATA TYPES
    # =====================================================

    def data_types(self):

        return pd.DataFrame(

            self.df.dtypes,

            columns=["Datatype"]

        )


    # =====================================================
    # MISSING VALUES
    # =====================================================

    def missing_values(self):

        return pd.DataFrame({

            "Missing Values":

            self.df.isnull().sum()

        })


    # =====================================================
    # DUPLICATES
    # =====================================================

    def duplicates(self):

        return self.df.duplicated().sum()