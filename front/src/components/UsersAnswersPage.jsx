import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getUserAnswers } from "../api";

export default function UserAnswersPage() {
  const { id } = useParams();
  const [answers, setAnswers] = useState([]);

  useEffect(() => {
    getUserAnswers(id).then(setAnswers);
  }, [id]);

  return (
    <div>
      <h2>Ответы пользователя #{id}</h2>
      {answers.length === 0 ? (
        <p>Нет ответов</p>
      ) : (
        <ul>
          {answers.map((a, i) => (
            <li key={i}>
              <Link to={`/quiz/${a.id}?user_id=${id}`}>{a.title}</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
