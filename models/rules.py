def generate_rules(metrics, clusters=None):

    insights = []

    total_revenue = metrics.get("total_revenue", 0)
    avg_discount = metrics.get("average_discount", 0)
    total_customers = metrics.get("total_customers", 0)
    avg_revenue = metrics.get("average_revenue", 0)
    top_location = metrics.get("top_location")

    # revenue health
    if total_revenue < 10000:
        insights.append(
            "Revenue is currently low. Consider improving acquisition campaigns and repeat purchases."
        )

    elif total_revenue > 100000:
        insights.append(
            "Revenue performance is strong. This may be a good time to scale paid marketing."
        )

    # discount dependency
    if avg_discount > 30:
        insights.append(
            "Heavy discount usage may be hurting profitability. Consider optimizing pricing strategy."
        )

    elif avg_discount < 10:
        insights.append(
            "Low discount dependency suggests stronger pricing power and healthier margins."
        )

    # customer base
    if total_customers < 20:
        insights.append(
            "Customer base is small. Focus on acquisition and retention campaigns."
        )

    elif total_customers > 100:
        insights.append(
            "You have a healthy customer base. Focus on segmentation and customer lifetime value."
        )

    # average order value
    if avg_revenue > 3000:
        insights.append(
            "Average customer spending is high. Premium targeting strategies may work well."
        )

    elif avg_revenue < 1000:
        insights.append(
            "Average spending is relatively low. Upselling and bundling strategies could help."
        )

    # top market
    if top_location:
        insights.append(
            f"{top_location} is your strongest market. Expanding campaigns there may increase ROI."
        )

    # segmentation intelligence
    if clusters:

        for cluster in clusters:

            segment = cluster.get("segment")
            customers = cluster.get("customers", 0)
            avg_cluster_revenue = cluster.get("avg_revenue", 0)

            if segment == "Premium Customers":
                insights.append(
                    f"Premium Customers generate high value with average spend around ₹{avg_cluster_revenue}."
                )

            elif segment == "Discount Hunters":
                insights.append(
                    "Discount Hunters respond strongly to promotions but may reduce profit margins."
                )

            elif customers < 5:
                insights.append(
                    f"The segment '{segment}' is very small. More data may improve clustering quality."
                )

    return insights