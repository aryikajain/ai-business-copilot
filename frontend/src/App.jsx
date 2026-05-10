import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Landing from "./pages/Landing";
import Auth from "./pages/Auth";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";

export default function App() {
  const token = localStorage.getItem("token");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/upload" element={token ? <Upload /> : <Navigate to="/auth" />} />
        <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/auth" />} />
        <Route path="/chat" element={token ? <Chat /> : <Navigate to="/auth" />} />
      </Routes>
    </Router>
  );
}
// function App() {
//   return (
//     <div className="min-h-screen flex items-center justify-center">
//       <h1 className="text-6xl font-bold text-blue-600">
//         AI Business Copilot 🚀
//       </h1>
//     </div>
//   );
// }

// export default App;