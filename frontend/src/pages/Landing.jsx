import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#f8fafc",
        padding: "40px",
      }}
    >
      <div
        style={{
          maxWidth: "800px",
          textAlign: "center",
        }}
      >
        <h1 style={{ fontSize: "48px", marginBottom: "20px" }}>
          AI Business Copilot
        </h1>

        <p
          style={{
            fontSize: "18px",
            color: "#555",
            lineHeight: "1.6",
            marginBottom: "30px",
          }}
        >
          Upload your business data, generate instant metrics, uncover customer insights,
          and get AI-powered recommendations to improve growth, ads, and strategy.
        </p>

        <button
          onClick={() => navigate("/auth")}
          style={{
            padding: "14px 28px",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
            fontSize: "16px",
            fontWeight: "bold",
          }}
        >
          Get Started
        </button>
      </div>
    </div>
  );
}
