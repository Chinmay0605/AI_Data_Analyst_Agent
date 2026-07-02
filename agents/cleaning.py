import pandas as pd


def clean_data(df):

    cleaned_df = df.copy()

    report = {}

    # Before Cleaning
    report["rows_before"] = cleaned_df.shape[0]

    # Remove duplicates
    duplicate_count = cleaned_df.duplicated().sum()
    cleaned_df = cleaned_df.drop_duplicates()

    report["duplicates_removed"] = duplicate_count

    # Remove completely empty columns
    empty_columns = cleaned_df.columns[cleaned_df.isnull().all()].tolist()

    cleaned_df = cleaned_df.drop(columns=empty_columns)

    report["empty_columns_removed"] = len(empty_columns)

    # Fill Missing Values
    filled = 0

    for column in cleaned_df.columns:

        if cleaned_df[column].dtype == "object":

            missing = cleaned_df[column].isnull().sum()

            if missing > 0:
                cleaned_df[column] = cleaned_df[column].fillna(
                    cleaned_df[column].mode()[0]
                )
                filled += missing

        else:

            missing = cleaned_df[column].isnull().sum()

            if missing > 0:
                cleaned_df[column] = cleaned_df[column].fillna(
                    cleaned_df[column].median()
                )
                filled += missing

    report["missing_values_filled"] = filled

    # ----------------------------
    # Clean Phone Numbers
    # ----------------------------
    if "Phone" in cleaned_df.columns:

        cleaned_df["Phone"] = (
            cleaned_df["Phone"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.replace(r"\D", "", regex=True)
        )

        cleaned_df["Phone"] = cleaned_df["Phone"].apply(
            lambda x: x[-10:] if len(x) >= 10 else x
        )

    report["rows_after"] = cleaned_df.shape[0]

    return cleaned_df, report