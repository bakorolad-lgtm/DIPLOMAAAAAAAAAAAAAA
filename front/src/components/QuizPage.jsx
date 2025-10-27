import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getQuizzes, getQuizCheckAnswers, sendQuizAnswers } from "../api";
import { useAuth } from "../context/AuthContext";

export default function QuizPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const all = await getQuizzes();
      const q = all.find((x) => x.id === parseInt(id));
      setQuiz(q);
      try {
        const check = await getQuizCheckAnswers(q.id, user);
        if (check.length > 0) setResults(check);
      } catch {}
      setLoading(false);
    }
    load();
  }, [id, user]);

  const handleChange = (qid, ans) => setAnswers((a) => ({ ...a, [qid]: ans }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = Object.entries(answers).map(([question_id, answer]) => ({
      question_id: parseInt(question_id),
      answer,
    }));
    await sendQuizAnswers(quiz.id, payload);
    const res = await getQuizCheckAnswers(quiz.id, user);
    setResults(res);
  };

  if (loading) return <p>Загрузка...</p>;
  if (!quiz) return <p>Тест не найден</p>;

  return (
    <div>
      <h2>{quiz.title}</h2>
      {results ? (
        <div>
          <h3>Результаты</h3>
          {results.map((r, i) => (
            <div key={i}>
              <strong>{r.title}</strong> —{" "}
              {r.is_correct ? "✅ Верно" : "❌ Неверно"}
            </div>
          ))}
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          {quiz.questions.map((q) => (
            <div key={q.id} style={{ marginBottom: 15 }}>
              <strong>{q.title}</strong>
              {q.answers.map((a) => (
                <div key={a}>
                  <label>
                    <input
                      type="radio"
                      name={`q${q.id}`}
                      value={a}
                      checked={answers[q.id] === a}
                      onChange={() => handleChange(q.id, a)}
                    />
                    {a}
                  </label>
                </div>
              ))}
            </div>
          ))}
          <button type="submit">Отправить</button>
        </form>
      )}
    </div>
  );
}
