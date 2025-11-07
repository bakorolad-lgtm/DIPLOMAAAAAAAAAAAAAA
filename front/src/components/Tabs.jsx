import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Tabs() {
  const { role } = useAuth();

  const { pathname } = useLocation();
  return (
    <nav style={{ marginBottom: 20 }}>
      <Link
        to="/"
        style={{
          marginRight: 10,
          textDecoration: pathname === "/" ? "underline" : "none",
        }}
      >
        Курсы
      </Link>
      <Link
        to="/quizzes"
        style={{
          marginRight: 10,
          textDecoration: pathname.startsWith("/quiz") ? "underline" : "none",
        }}
      >
        Тесты
      </Link>
      { role === "admin" && (
        <Link
          to="/users"
          style={{
            textDecoration: pathname.startsWith("/users") ? "underline" : "none",
          }}
        >
          Пользователи
        </Link>
      )}
    </nav>
  );
}
