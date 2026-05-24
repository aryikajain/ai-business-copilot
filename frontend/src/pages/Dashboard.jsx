import { useEffect, useMemo, useState } from "react";

import Navbar from "../components/Navbar";
import KPIBox from "../components/KPIBox";
import ChartCard from "../components/ChartCard";
import AIRecommendationCard from "../components/AIRecommendationCard";

import API from "../api";

import {
  DollarSign,
  Users,
  MapPin,
  Percent,
  Sparkles,
  BarChart3,
  TrendingUp,
} from "lucide-react";

export default function Dashboard() {

  const [analysis, setAnalysis] = useState(null);

  // FETCH DASHBOARD DATA
  useEffect(() => {

    const fetchDashboard = async () => {

      try {

        const user_id = localStorage.getItem("user_id");

        const response = await API.get(
          `/dashboard/${user_id}`
        );

        setAnalysis(response.data);

      } catch (error) {

        console.error(error);

      }
    };

    fetchDashboard();

  }, []);

  // RAW DATA
  const chartData = useMemo(() => {
    return analysis?.debug?.clean_preview || [];
  }, [analysis]);

  // REVENUE BY CITY
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

        acc[city].revenue += Number(
          row.amount_spent || 0
        );

        return acc;

      }, {})
    );

  }, [chartData]);

  // REAL ML SEGMENTS
  const customerSegments = useMemo(() => {

    return analysis?.clusters || [];

  }, [analysis]);

  // LOADING / EMPTY STATE
  if (!analysis) {

    return (
      <>
        <Navbar />

        <div className="min-h-screen bg-slate-50 flex items-center justify-center">

          <div className="text-center">

            <BarChart3
              size={60}
              className="mx-auto text-blue-600 mb-5"
            />

            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              Loading Dashboard...
            </h2>

            <p className="text-gray-500">
              Fetching business intelligence data
            </p>

          </div>
        </div>
      </>
    );
  }

  // METRICS
  const metrics = analysis.metrics || {};

  // INSIGHTS
  const insights = analysis.insights || [];

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-slate-50 px-6 py-10">

        {/* HEADER */}
        <div className="max-w-7xl mx-auto mb-10">

          <div className="flex items-center gap-4 mb-4">

            <div className="bg-blue-100 p-4 rounded-3xl">
              <TrendingUp
                size={36}
                className="text-blue-600"
              />
            </div>

            <div>
              <h1 className="text-5xl font-bold text-gray-900">
                Business Dashboard
              </h1>

              <p className="text-gray-500 text-lg mt-2">
                AI-powered business intelligence overview
              </p>
            </div>
          </div>
        </div>

        {/* KPI GRID */}
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">

          <KPIBox
            title="Total Revenue"
            value={`₹${metrics.total_revenue?.toFixed(2)}`}
            icon={<DollarSign />}
          />

          <KPIBox
            title="Revenue / Customer"
            value={`₹${metrics.revenue_per_customer || 0}`}
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
            title="Average Revenue"
            value={`₹${metrics.average_revenue?.toFixed(2)}`}
            icon={<Sparkles />}
          />

          <KPIBox
            title="Average Discount"
            value={`${metrics.average_discount?.toFixed(1)}%`}
            icon={<Percent />}
          />

          <KPIBox
            title="Market Reach"
            value={metrics.total_locations}
            icon={<MapPin />}
          />

          <KPIBox
            title="Average Age"
            value={metrics.average_age}
            icon={<Users />}
          />
        </div>

        {/* INSIGHTS */}
        <div className="max-w-7xl mx-auto bg-white rounded-3xl shadow-sm p-8 mb-10">

          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            AI Business Insights
          </h2>

          <div className="space-y-4">

            {insights.map((item, index) => (

              <div
                key={index}
                className="bg-slate-50 border border-slate-200 rounded-2xl p-5"
              >
                <p className="text-gray-700 leading-relaxed">
                  {item}
                </p>
              </div>

            ))}
          </div>
        </div>

        {/* AI RECOMMENDATIONS */}
        <div className="max-w-7xl mx-auto mb-10">

          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            AI Recommendations
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

            <AIRecommendationCard
              title="Scale High-Performing Markets"
              description={`${
                metrics.top_location
              } is currently your strongest market. Increasing localized campaigns there could improve ROI.`}
            />

            <AIRecommendationCard
              title="Optimize Discount Strategy"
              description="Heavy discount usage may reduce profit margins. Consider testing lower promotional dependency."
            />

            <AIRecommendationCard
              title="Focus on Premium Segments"
              description="Your high-value customer clusters contribute disproportionately to revenue. Build retention strategies around them."
            />

          </div>
        </div>

        {/* CHARTS */}
        <div className="max-w-7xl mx-auto grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">

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

        {/* SEGMENT TABLE */}
        <div className="max-w-7xl mx-auto bg-white rounded-3xl shadow-sm p-8">

          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Customer Segment Analysis
          </h2>

          <div className="overflow-x-auto">

            <table className="w-full">

              <thead>

                <tr className="border-b border-gray-200 text-left">

                  <th className="pb-4 font-semibold text-gray-700">
                    Segment
                  </th>

                  <th className="pb-4 font-semibold text-gray-700">
                    Customers
                  </th>

                  <th className="pb-4 font-semibold text-gray-700">
                    Avg Revenue
                  </th>

                  <th className="pb-4 font-semibold text-gray-700">
                    Avg Discount
                  </th>

                </tr>

              </thead>

              <tbody>

                {analysis?.clusters?.map((cluster, index) => (

                  <tr
                    key={index}
                    className="border-b border-gray-100"
                  >

                    <td className="py-5 font-semibold text-gray-900">
                      {cluster.segment}
                    </td>

                    <td className="py-5 text-gray-700">
                      {cluster.customers}
                    </td>

                    <td className="py-5 text-gray-700">
                      ₹{cluster.avg_revenue}
                    </td>

                    <td className="py-5 text-gray-700">
                      {cluster.avg_discount}%
                    </td>

                  </tr>

                ))}

              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}