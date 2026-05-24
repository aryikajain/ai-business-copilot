def calculate_metrics(df, mapping):

    metrics = {}

    revenue_col = mapping.get("revenue")
    location_col = mapping.get("location")
    customer_col = mapping.get("customer")
    discount_col = mapping.get("discount")
    age_col = mapping.get("age")

    # revenue metrics
    if revenue_col:

        metrics["total_revenue"] = round(
            float(df[revenue_col].sum()),
            2
        )

        metrics["average_revenue"] = round(
            float(df[revenue_col].mean()),
            2
        )

        metrics["highest_revenue"] = round(
            float(df[revenue_col].max()),
            2
        )

        metrics["lowest_revenue"] = round(
            float(df[revenue_col].min()),
            2
        )

        metrics["revenue_std"] = round(
            float(df[revenue_col].std()),
            2
        )

    # location metrics
    if location_col:

        metrics["top_location"] = (
            df[location_col]
            .mode()[0]
        )

        metrics["total_locations"] = (
            df[location_col]
            .nunique()
        )

    # customer metrics
    if customer_col:

        metrics["total_customers"] = (
            df[customer_col]
            .nunique()
        )

    # discount metrics
    if discount_col:

        metrics["average_discount"] = round(
            float(df[discount_col].mean()),
            2
        )

        metrics["max_discount"] = round(
            float(df[discount_col].max()),
            2
        )

    # age metrics
    if age_col:

        metrics["average_age"] = round(
            float(df[age_col].mean()),
            2
        )

        metrics["youngest_customer"] = int(
            df[age_col].min()
        )

        metrics["oldest_customer"] = int(
            df[age_col].max()
        )

    # derived business intelligence

    if (
        revenue_col
        and customer_col
        and metrics["total_customers"] > 0
    ):

        metrics["revenue_per_customer"] = round(
            metrics["total_revenue"] /
            metrics["total_customers"],
            2
        )

    return metrics