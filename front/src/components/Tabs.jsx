import { Link, useLocation } from "react-router-dom";

export default function Tabs() {
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
          textDecoration: pathname.startsWith("/quiz") ? "underline" : "none",
        }}
      >
        Тесты
      </Link>
    </nav>
  );
}
