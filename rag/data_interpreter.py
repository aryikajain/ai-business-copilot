import pandas as pd
import numpy as np


def load_csv(file_path):

    """
    Load CSV safely
    """

    return pd.read_csv(file_path)


def clean_data(df):

    """
    Advanced business data cleaning
    """

    cleaning_report = {
        "rows_before": len(df),
        "duplicates_removed": 0,
        "pii_columns_removed": [],
        "outliers_detected": {},
        "missing_values_filled": {},
    }

    # normalize columns
    df.columns = [
        col.strip()
        .lower()
        .replace(" ", "_")
        for col in df.columns
    ]

    # remove empty rows
    df = df.dropna(how="all")

    # remove duplicates
    before_duplicates = len(df)

    df = df.drop_duplicates()

    cleaning_report["duplicates_removed"] = (
        before_duplicates - len(df)
    )

    # remove PII
    pii_keywords = [
        "phone",
        "email",
        "password",
        "address",
    ]

    drop_cols = [
        col for col in df.columns
        if any(
            keyword in col
            for keyword in pii_keywords
        )
    ]

    cleaning_report["pii_columns_removed"] = drop_cols

    df = df.drop(
        columns=drop_cols,
        errors="ignore"
    )

    # trim strings
    for col in df.columns:

        if df[col].dtype == "object":

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    # smart numeric conversion
    for col in df.columns:

        if df[col].dtype == "object":

            cleaned = (
                df[col]
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace("%", "", regex=False)
            )

            numeric_version = pd.to_numeric(
                cleaned,
                errors="coerce"
            )

            # convert only if majority numeric
            if (
                numeric_version.notna().sum()
                > len(df) * 0.6
            ):

                df[col] = numeric_version

    # remove constant columns
    constant_cols = [
        col for col in df.columns
        if df[col].nunique() <= 1
    ]

    df = df.drop(
        columns=constant_cols,
        errors="ignore"
    )

    # missing values
    for col in df.columns:

        missing_count = df[col].isna().sum()

        if missing_count > 0:

            cleaning_report[
                "missing_values_filled"
            ][col] = int(missing_count)

        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(
                df[col].median()
            )

        else:

            mode_val = df[col].mode()

            df[col] = df[col].fillna(
                mode_val[0]
                if not mode_val.empty
                else "unknown"
            )

    # OUTLIER DETECTION ONLY
    # do NOT remove automatically
    numeric_cols = df.select_dtypes(
        include=[np.number]
    ).columns

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outlier_count = len(
            df[
                (df[col] < lower)
                | (df[col] > upper)
            ]
        )

        cleaning_report[
            "outliers_detected"
        ][col] = int(outlier_count)

    cleaning_report["rows_after"] = len(df)

    return (
        df.reset_index(drop=True),
        cleaning_report
    )


def detect_columns(df):

    """
    Intelligent business schema detection
    """

    mapping = {}

    revenue_keywords = [
        "amount",
        "price",
        "revenue",
        "sales",
        "income",
        "spend",
        "profit",
        "transaction",
    ]

    customer_keywords = [
        "customer",
        "client",
        "buyer",
        "name",
        "user",
    ]

    location_keywords = [
        "city",
        "location",
        "state",
        "country",
        "region",
    ]

    discount_keywords = [
        "discount",
        "coupon",
        "offer",
        "promo",
    ]

    for col in df.columns:

        c = col.lower()

        if any(k in c for k in revenue_keywords):
            mapping["revenue"] = col

        elif any(k in c for k in customer_keywords):
            mapping["customer"] = col

        elif any(k in c for k in location_keywords):
            mapping["location"] = col

        elif "age" in c:
            mapping["age"] = col

        elif "gender" in c:
            mapping["gender"] = col

        elif any(k in c for k in discount_keywords):
            mapping["discount"] = col

    return mapping