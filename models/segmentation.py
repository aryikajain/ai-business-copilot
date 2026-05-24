from sklearn.preprocessing import StandardScaler
from sklearn.cluster import (
    KMeans,
    DBSCAN,
    AgglomerativeClustering,
)


def customer_segmentation(df, mapping, method="kmeans"):

    feature_cols = []

    if "revenue" in mapping:
        feature_cols.append(mapping["revenue"])

    if "age" in mapping:
        feature_cols.append(mapping["age"])

    if "discount" in mapping:
        feature_cols.append(mapping["discount"])

    if len(feature_cols) < 1:
        return None

    # prepare data
    data = df[feature_cols].copy()

    if len(data) < 2:
        return None

    # scale features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    if method == "auto":
        method = "kmeans"

    # choose model
    if method == "kmeans":
        model = KMeans(
            n_clusters=min(3, len(data)),
            random_state=42,
            n_init=10
        )

    elif method == "dbscan":
        model = DBSCAN(
            eps=0.8,
            min_samples=5
        )

    elif method == "hierarchical":
        model = AgglomerativeClustering(
            n_clusters=3
        )

    else:
        return None

    # clustering
    df["cluster"] = model.fit_predict(scaled_data)

    # create business labels
    segment_labels = {}

    cluster_summary = []

    for cluster_id in sorted(df["cluster"].unique()):

        cluster_df = df[df["cluster"] == cluster_id]

        avg_revenue = (
            cluster_df[mapping["revenue"]].mean()
            if "revenue" in mapping
            else 0
        )

        avg_discount = cluster_df[
            mapping["discount"]
        ].mean() if "discount" in mapping else 0

        customer_count = len(cluster_df)

        # business interpretation
        if avg_revenue > 3000:
            segment_name = "Premium Customers"

        elif avg_discount > 35:
            segment_name = "Discount Hunters"

        else:
            segment_name = "Regular Customers"

        segment_labels[cluster_id] = segment_name

        cluster_summary.append({
            "cluster_id": int(cluster_id),
            "segment": segment_name,
            "customers": customer_count,
            "avg_revenue": round(float(avg_revenue), 2),
            "avg_discount": round(float(avg_discount), 2),
        })

    # map cluster names
    df["segment"] = df["cluster"].map(segment_labels)

    return {
        "segmented_df": df,
        "cluster_summary": cluster_summary
    }
