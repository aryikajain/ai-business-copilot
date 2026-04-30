# Metrics calculation will be implemented here
def calculate_metrics(df, mapping):
    metrics = {}

    revenue_col = mapping.get("revenue")
    location_col = mapping.get("location")
    customer_col = mapping.get("customer")
    discount_col = mapping.get("discount")

    if revenue_col:
        metrics["total_revenue"] = df[revenue_col].sum()
        metrics["average_revenue"] = df[revenue_col].mean()

    if location_col:
        metrics["top_location"] = df[location_col].mode()[0]

    if customer_col:
        metrics["total_customers"] = df[customer_col].nunique()

    if discount_col:
        metrics["average_discount"] = df[discount_col].mean()

    return metrics