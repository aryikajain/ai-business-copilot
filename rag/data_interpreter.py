import pandas as pd
import numpy as np


def load_csv(file_path):
    return pd.read_csv(file_path)


def clean_data(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.dropna(how="all")
    df = df.drop_duplicates()

    drop_cols = [col for col in df.columns if "phone" in col or "email" in col]
    df = df.drop(columns=drop_cols, errors="ignore")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    for col in df.columns:
        if df[col].dtype == "object":
            cleaned = (
                df[col]
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace("%", "", regex=False)
            )

            numeric_version = pd.to_numeric(cleaned, errors="coerce")

            if numeric_version.notna().sum() > len(df) * 0.5:
                df[col] = numeric_version

    for col in df.columns:
        if df[col].nunique() <= 1:
            df = df.drop(columns=[col])

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode_val = df[col].mode()
            df[col] = df[col].fillna(mode_val[0] if not mode_val.empty else "unknown")

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df = df[(df[col] >= lower) & (df[col] <= upper)]

    return df.reset_index(drop=True)


def detect_columns(df):
    mapping = {}

    for col in df.columns:
        c = col.lower()

        if "amount" in c or "price" in c or "revenue" in c:
            mapping["revenue"] = col
        elif "customer" in c or "name" in c:
            mapping["customer"] = col
        elif "city" in c or "location" in c:
            mapping["location"] = col
        elif "age" in c:
            mapping["age"] = col
        elif "gender" in c:
            mapping["gender"] = col
        elif "discount" in c:
            mapping["discount"] = col

    return mapping