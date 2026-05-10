import { useEffect, useMemo, useState } from "react";

import Navbar from "../components/Navbar";
import KPIBox from "../components/KPIBox";
import ChartCard from "../components/ChartCard";
import AIRecommendationCard from "../components/AIRecommendationCard";

import {
  DollarSign,
  Users,
  MapPin,
  Percent,
  Sparkles,
} from "lucide-react";

export default function Dashboard() {
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem("analysis");

    if (stored) {
      setAnalysis(JSON.parse(stored));
    }
  }, []);

  const chartData = useMemo(() => {
    return analysis?.debug?.clean_preview || [];
  }, [analysis]);

  const revenueByCity = useMemo(() => {
    return Object.values(
      chartData.reduce((acc, row) => {
        const city = row.city || "Unknown";

        if (!acc[city]) {
          acc[city] = {
            city,
            revenue: 0,
          };
        }

        acc[city].revenue += Number(row.amount_spent || 0);

        return acc;
      }, {})
    );
  }, [chartData]);

  const customerSegments = useMemo(() => {
    const grouped = {
      "High Value": 0,
      "Mid Value": 0,
      "Low Value": 0,
    };

    chartData.forEach((row) => {
      const spend = Number(row.amount_spent || 0);

      if (spend > 3000) grouped["High Value"] += 1;
      else if (spend > 1200) grouped["Mid Value"] += 1;
      else grouped["Low Value"] += 1;
    });

    return Object.entries(grouped).map(([segment, customers]) => ({
      segment,
      customers,
    }));
  }, [chartData]);

  if (!analysis) {
    return (
      <>
        <Navbar />

        <div className="p-10">
          <h2>No analysis found. Please upload a CSV first.</h2>
        </div>
      </>
    );
  }

  const metrics = analysis.metrics || {};
  const insights = analysis.insights || [];

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-slate-50 px-6 py-10">

        {/* Header */}
        <div className="max-w-7xl mx-auto mb-10">
          <h1 className="text-5xl font-bold text-gray-900 mb-3">
            Business Dashboard
          </h1>

          <p className="text-gray-500 text-lg">
            AI-powered analytics and business intelligence overview.
          </p>
        </div>

        {/* KPI GRID */}
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-6 mb-10">

          <KPIBox
            title="Total Revenue"
            value={`₹${metrics.total_revenue?.toFixed(2)}`}
            icon={<DollarSign />}
          />

          <KPIBox
            title="Average Revenue"
            value={`₹${metrics.average_revenue?.toFixed(2)}`}
            icon={<Percent />}
          />

          <KPIBox
            title="Top Location"
            value={metrics.top_location}
            icon={<MapPin />}
          />

          <KPIBox
            title="Customers"
            value={metrics.total_customers}
            icon={<Users />}
          />

          <KPIBox
            title="Avg Discount"
            value={`${metrics.average_discount?.toFixed(1)}%`}
            icon={<Sparkles />}
          />
        </div>

        {/* INSIGHTS */}
        <div className="max-w-7xl mx-auto bg-white rounded-3xl shadow-sm p-8 mb-10">

          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            AI Business Insights
          </h2>

          <div className="space-y-4">
            {insights.map((item, index) => (
              <div
                key={index}
                className="bg-slate-50 border border-slate-200 rounded-2xl p-5"
              >
                <p className="text-gray-700">{item}</p>
              </div>
            ))}
          </div>
        </div>
        
        {/* AI Recommendations */}
        <div className="max-w-7xl mx-auto mb-10">

        <h2 className="text-3xl font-bold text-gray-900 mb-6">
            AI Recommendations
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

            <AIRecommendationCard
            title="Scale Ads in Jaipur"
            description="Jaipur is currently your strongest revenue-generating location. Increasing localized campaigns here could improve ROI."
            />

            <AIRecommendationCard
            title="Reduce Discount Dependency"
            description="Average discount usage is relatively high. Excessive discounts may reduce long-term profitability."
            />

            <AIRecommendationCard
            title="Target High-Value Customers"
            description="Your high-spending customer segment contributes disproportionately to revenue. Build retention campaigns around them."
            />

        </div>
        </div>
        {/* CHARTS */}
        <div className="max-w-7xl mx-auto grid grid-cols-1 xl:grid-cols-2 gap-8">

          <ChartCard
            title="Revenue by Location"
            data={revenueByCity}
            dataKey="revenue"
            xKey="city"
          />

          <ChartCard
            title="Customer Segments"
            data={customerSegments}
            dataKey="customers"
            xKey="segment"
          />
        </div>
      </div>
    </>
  );
}