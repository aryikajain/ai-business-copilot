# Rules engine will be implemented here
def generate_rules(metrics):
    insights = []

    if metrics.get("total_revenue", 0) < 5000:
        insights.append("Revenue is low. Consider running local promotional campaigns.")

    if metrics.get("average_discount", 0) > 20:
        insights.append("Average discount is high. You may be reducing profit margins.")

    if metrics.get("total_customers", 0) < 20:
        insights.append("Customer base is small. Focus on customer acquisition and retention.")

    if metrics.get("top_location"):
        insights.append(f"Your strongest market is {metrics['top_location']}. Increase ad spend there.")

    return insights