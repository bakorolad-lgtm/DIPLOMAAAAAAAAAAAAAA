import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getQuizzes } from "../api";

export default function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    getQuizzes().then(setQuizzes);
  }, []);

  return (
    <div>
      <h2>Тесты</h2>
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
