import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bot } from "lucide-react";
import API from "../api";

export default function Auth() {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = async () => {
    try {
      const endpoint = isLogin ? "/auth/login" : "/auth/register";

      const response = await API.post(endpoint, {
        email,
        password,
      });

      if (isLogin) {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("user_id", response.data.user.user_id);

        navigate("/upload");
      } else {
        alert("Registered successfully. Please login.");
        setIsLogin(true);
      }
    } catch (error) {
      alert(error.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-6">

      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl p-10">

        {/* Logo */}
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-blue-600 p-3 rounded-2xl text-white">
            <Bot size={28} />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              AI Business Copilot
            </h1>

            <p className="text-sm text-gray-500">
              Business Intelligence Platform
            </p>
          </div>
        </div>

        {/* Heading */}
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          {isLogin ? "Welcome back" : "Create account"}
        </h2>

        <p className="text-gray-500 mb-8">
          {isLogin
            ? "Login to continue analyzing your business."
            : "Start generating AI-powered business insights."}
        </p>

        {/* Email */}
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-4 border border-gray-200 rounded-2xl mb-4 outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Password */}
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-4 border border-gray-200 rounded-2xl mb-6 outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Button */}
        <button
          onClick={handleAuth}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 rounded-2xl transition-all duration-200"
        >
          {isLogin ? "Login" : "Create Account"}
        </button>

        {/* Toggle */}
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="w-full mt-5 text-blue-600 hover:text-blue-700 text-sm font-medium"
        >
          {isLogin
            ? "New here? Create an account"
            : "Already have an account? Login"}
        </button>
      </div>
    </div>
  );
}