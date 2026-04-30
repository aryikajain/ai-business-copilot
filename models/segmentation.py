from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering


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

    data = df[feature_cols].copy()

    # scale features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # choose clustering method
    if method == "kmeans":
        model = KMeans(n_clusters=3, random_state=42, n_init=10)

    elif method == "dbscan":
        model = DBSCAN(eps=0.8, min_samples=5)

    elif method == "hierarchical":
        model = AgglomerativeClustering(n_clusters=3)

    else:
        return None

    df["cluster"] = model.fit_predict(scaled_data)

    return df