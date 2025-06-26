import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import type { ReactNode } from "react";
import Profile from "./pages/Profile";
import AdminRoute from "./components/AdminRoute";
import EditProfile from "./pages/EditProfile";
import Leaderboard from "./pages/leaderboard/Leaderboard";
import MatchHistory from "./pages/history/MatchHistory";



const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  return user ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/admin" element={<AdminRoute><div>Admin Panel</div></AdminRoute>} />
          <Route
  path="/profile/edit"
  element={
    <ProtectedRoute>
      <EditProfile />
    </ProtectedRoute>
  }
/>
<Route path="/leaderboard" element={<Leaderboard />} />
<Route
  path="/history"
  element={
    <ProtectedRoute>
      <MatchHistory />
    </ProtectedRoute>
  }
/>


          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
