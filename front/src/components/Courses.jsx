import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getCourses } from "../api";
import { useAuth } from "../context/AuthContext";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const { role } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    getCourses().then(setCourses);
  }, []);

  const truncate = (text, maxLength = 50) => {
    if (!text) return "";
    return text.length > maxLength ? text.slice(0, maxLength) + "…" : text;
  };

  return (
    <div>
      <h2>Курсы</h2>
      { role === "admin" && (
          <button type="button" onClick={() => navigate("/courses/new")}>Создать</button>
        )
      }
      {courses.length === 0 && <p>Нет курсов</p>}
      <ul>
        {courses.map((c, i) => (
          <li key={i} style={{ marginBottom: "10px" }}>
            <Link to={`/course/${c.id || i}`} style={{ fontWeight: "bold" }}>
              {c.title}
            </Link>
            <div style={{ color: "#555", fontSize: "0.9em" }}>
              {truncate(c.description, 50)}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
