import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getQuizzes } from "../api";
import { useAuth } from "../context/AuthContext";

export default function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const { role } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    getQuizzes().then(setQuizzes);
  }, []);

  return (
    <div>
      <h2>Тесты</h2>
      { role === "admin" && (
          <button type="button" onClick={() => navigate("/quiz/new")}>Создать</button>
        )
      }
      <ul>
        {quizzes.map((q) => (
          <li key={q.id}>
            <Link to={`/quiz/${q.id}`}>{q.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
