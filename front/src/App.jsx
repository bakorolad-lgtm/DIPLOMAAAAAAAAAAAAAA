import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Tabs from "./components/Tabs";
import Courses from "./components/Courses";
import CoursePage from "./components/CoursePage";
import Quizzes from "./components/Quizzes";
import QuizPage from "./components/QuizPage";
import AuthPage from "./components/AuthPage";
import { useAuth, AuthProvider } from "./context/AuthContext";
import Users from "./components/Users";
import UsersAnswersPage from "./components/UsersAnswersPage";
import CreateCoursePage from "./components/CourseCreate";
import CreateQuizPage from "./components/QuizCreate";

function ProtectedRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/auth" />;
}

function AppRoutes() {
  const { user, signOut, role } = useAuth();

  return (
    <div className="container" style={{
      backgroundColor: "#b7b7b7ff", // светло-серый фон
      minHeight: "100vh", // растянуть на весь экран
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
    }}>
      <h1>Учебный портал</h1>
      {user && (
        <div style={{ marginBottom: 10 }}>
          Привет, {user}! <button onClick={signOut}>Выйти</button>
        </div>
      )}
      {user && (
        <Tabs />
      )}
      <h1>{role}</h1>
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
        {role === "admin" && (
          <>
            <Route
              path="/users"
              element={
                <ProtectedRoute>
                  <Users />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quiz/user/answers/:id"
              element={
                <ProtectedRoute>
                  <UsersAnswersPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/courses/new"
              element = {
                <ProtectedRoute>
                  <CreateCoursePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quiz/new"
              element = {
                <ProtectedRoute>
                  <CreateQuizPage />
                </ProtectedRoute>
              }
            />
          </>
        )}
        
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
