from rag.data_interpreter import load_csv, clean_data, detect_columns
from models.metrics import calculate_metrics
from models.rules import generate_rules
from models.segmentation import customer_segmentation
import math
import numpy as np


def make_json_safe(value):
    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    if isinstance(value, tuple):
        return [make_json_safe(item) for item in value]

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        value = float(value)

    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None

    return value


def process_file(file_path):
    # 1. load raw
    raw_df = load_csv(file_path)

    # 2. clean
    clean_df, cleaning_report = clean_data(raw_df.copy())

    # 3. detect business meaning
    mapping = detect_columns(clean_df)

    # 4. calculate KPIs
    metrics = calculate_metrics(clean_df, mapping)

    # 5. business rules
    insights = generate_rules(metrics)

    # 6. segmentation
    segmentation = customer_segmentation(clean_df.copy(), mapping, method="auto")

    segmented_df = None
    cluster_summary = []
    cluster_preview = []

    if segmentation:
        segmented_df = segmentation.get("segmented_df")
        cluster_summary = segmentation.get("cluster_summary", [])

    if segmented_df is not None and "cluster" in segmented_df.columns:
        cluster_preview = segmented_df.head(10).to_dict(orient="records")

    return make_json_safe({
        "columns": list(clean_df.columns),
        "mapping": mapping,
        "rows_before_cleaning": len(raw_df),
        "rows_after_cleaning": len(clean_df),
        "cleaning_report": cleaning_report,
        "metrics": metrics,
        "insights": insights,
        "clusters": cluster_summary,

        # debug proof
        "debug": {
            "raw_preview": raw_df.head(5).to_dict(orient="records"),
            "clean_preview": clean_df.head(5).to_dict(orient="records"),
            "cluster_preview": cluster_preview
        }
    })
