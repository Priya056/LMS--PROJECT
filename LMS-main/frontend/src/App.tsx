import { Navigate, Route, Routes } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "./auth";
import CoursePage from "./pages/CoursePage";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import ProblemPage from "./pages/ProblemPage";
import LecturePage from "./pages/LecturePage";
import Register from "./pages/Register";
import Shell from "./Shell";

function RequireAuth({ children }: { children: ReactNode }) {
  const { user, ready } = useAuth();
  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center text-slate-400">Loading…</div>
    );
  }
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/"
        element={
          <RequireAuth>
            <Shell />
          </RequireAuth>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="course/:slug" element={<CoursePage />} />
        <Route path="course/:slug/lecture/:number" element={<LecturePage />} />
        <Route path="problem/:id" element={<ProblemPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
