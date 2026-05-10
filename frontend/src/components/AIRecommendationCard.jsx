export default function AIRecommendationCard({
  title,
  description,
}) {
  return (
    <div className="bg-white rounded-3xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200">

      <h3 className="text-xl font-bold text-gray-900 mb-3">
        {title}
      </h3>

      <p className="text-gray-600 leading-relaxed">
        {description}
      </p>
    </div>
  );
}