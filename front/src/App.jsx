import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Tabs from "./components/Tabs";
import Courses from "./components/Courses";
import CoursePage from "./components/CoursePage";
import Quizzes from "./components/Quizzes";
import QuizPage from "./components/QuizPage";
import AuthPage from "./components/AuthPage";
import { useAuth, AuthProvider } from "./context/AuthContext";

function ProtectedRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/auth" />;
}

function AppRoutes() {
  const { user, signOut } = useAuth();

  return (
    <div className="container">
      <h1>Учебный портал</h1>
      {user && (
        <div style={{ marginBottom: 10 }}>
          Привет, {user}! <button onClick={signOut}>Выйти</button>
        </div>
      )}
      <Tabs />
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Courses />
            </ProtectedRoute>
          }
        />
        <Route
          path="/course/:id"
          element={
            <ProtectedRoute>
              <CoursePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/quizzes"
          element={
            <ProtectedRoute>
              <Quizzes />
            </ProtectedRoute>
          }
        />
        <Route
          path="/quiz/:id"
          element={
            <ProtectedRoute>
              <QuizPage />
            </ProtectedRoute>
          }
        />
        <Route path="/auth" element={<AuthPage />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}
