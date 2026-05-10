import { useState } from "react";
import { Bot, User, SendHorizonal } from "lucide-react";

import Navbar from "../components/Navbar";
import API from "../api";

export default function Chat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query.trim()) return;

    const user_id = localStorage.getItem("user_id");

    const userMessage = {
      type: "user",
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentQuery = query;
    setQuery("");

    try {
      setLoading(true);

      const response = await API.post("/chat", {
        user_id,
        query: currentQuery,
      });

      const aiMessage = {
        type: "ai",
        text: response.data.answer,
        context: response.data.context || [],
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: "AI request failed. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-slate-50 px-6 py-10">

        <div className="max-w-5xl mx-auto">

          {/* Header */}
          <div className="mb-8">
            <h1 className="text-5xl font-bold text-gray-900 mb-3">
              AI Business Chat
            </h1>

            <p className="text-gray-500 text-lg">
              Ask questions about your customers, revenue, growth, and strategy.
            </p>
          </div>

          {/* Chat Container */}
          <div className="bg-white rounded-3xl shadow-sm border border-gray-200 flex flex-col h-[700px]">

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">

              {messages.length === 0 && (
                <div className="h-full flex items-center justify-center text-center">

                  <div>
                    <div className="w-20 h-20 bg-blue-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
                      <Bot size={40} className="text-blue-600" />
                    </div>

                    <h2 className="text-2xl font-bold text-gray-900 mb-3">
                      Start chatting with your AI copilot
                    </h2>

                    <p className="text-gray-500">
                      Ask about business strategy, customer insights,
                      revenue growth, or ad optimization.
                    </p>
                  </div>
                </div>
              )}

              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.type === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[75%] rounded-3xl px-5 py-4 ${
                      msg.type === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-slate-100 text-gray-900"
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-2">

                      {msg.type === "user" ? (
                        <User size={18} />
                      ) : (
                        <Bot size={18} />
                      )}

                      <span className="font-semibold text-sm">
                        {msg.type === "user" ? "You" : "AI Copilot"}
                      </span>
                    </div>

                    <p className="leading-relaxed">
                      {msg.text}
                    </p>

                    {/* Context */}
                    {msg.type === "ai" &&
                      msg.context?.length > 0 && (
                        <div className="mt-4 border-t border-gray-300 pt-3">

                          <p className="text-xs font-semibold mb-2 text-gray-500">
                            BUSINESS CONTEXT USED
                          </p>

                          <ul className="space-y-1 text-sm text-gray-600">
                            {msg.context.map((item, i) => (
                              <li key={i}>• {item}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="text-gray-500">
                  AI is analyzing your business...
                </div>
              )}
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 p-5">

              <div className="flex items-center gap-4">

                <input
                  type="text"
                  placeholder="Ask about your business..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="flex-1 border border-gray-300 rounded-2xl px-5 py-4 outline-none focus:ring-2 focus:ring-blue-500"
                />

                <button
                  onClick={handleAsk}
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-2xl transition-all duration-200"
                >
                  <SendHorizonal size={22} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}