import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createQuiz } from "../api";

export default function CreateQuizPage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [questions, setQuestions] = useState([
    { title: "", answers: [""], correct_answer: "" },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const renumberQuestions = (list) =>
    list.map((q, i) => ({ ...q, id: i + 1 }));

  const handleQuestionChange = (index, field, value) => {
    const updated = [...questions];
    updated[index][field] = value;
    setQuestions(renumberQuestions(updated));
  };

  const handleAnswerChange = (qIndex, aIndex, value) => {
    const updated = [...questions];
    updated[qIndex].answers[aIndex] = value;
    setQuestions(renumberQuestions(updated));
  };

  const addQuestion = () => {
    const newQuestions = [
      ...questions,
      { id: questions.length + 1, title: "", answers: [""], correct_answer: "" },
    ];
    setQuestions(renumberQuestions(newQuestions));
  };

  const addAnswer = (qIndex) => {
    const updated = [...questions];
    updated[qIndex].answers.push("");
    setQuestions(renumberQuestions(updated));
  };

  const removeQuestion = (index) => {
    const updated = questions.filter((_, i) => i !== index);
    setQuestions(renumberQuestions(updated));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const quizData = {
        title,
        questions: questions.map((q) => ({
          id: q.id,
          title: q.title,
          answers: q.answers.filter((a) => a.trim() !== ""),
          correct_answer: q.correct_answer,
        })),
      };

      const newQuiz = await createQuiz(quizData);

      // Переходим на страницу созданного опроса
      navigate(`/quiz/${newQuiz.id}`, { state: { quiz: newQuiz } });
    } catch (err) {
      console.error(err);
      setError("Не удалось создать опрос");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Создание нового опроса</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Название опроса:
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </label>
        </div>

        {questions.map((q, qIndex) => (
          <div
            key={qIndex}
            style={{
              border: "1px solid #ccc",
              padding: 10,
              marginTop: 15,
              borderRadius: 8,
            }}
          >
            <label>
              Вопрос {qIndex + 1}:
              <input
                type="text"
                value={q.title}
                onChange={(e) =>
                  handleQuestionChange(qIndex, "title", e.target.value)
                }
                required
              />
            </label>

            <div style={{ marginTop: 10 }}>
              <strong>Ответы:</strong>
              {q.answers.map((a, aIndex) => (
                <div key={aIndex}>
                  <input
                    type="text"
                    value={a}
                    placeholder={`Ответ ${aIndex + 1}`}
                    onChange={(e) =>
                      handleAnswerChange(qIndex, aIndex, e.target.value)
                    }
                    required
                  />
                </div>
              ))}
              <button type="button" onClick={() => addAnswer(qIndex)}>
                ➕ Добавить ответ
              </button>
            </div>

            <div style={{ marginTop: 10 }}>
              <label>
                Правильный ответ:
                <input
                  type="text"
                  value={q.correct_answer}
                  onChange={(e) =>
                    handleQuestionChange(qIndex, "correct_answer", e.target.value)
                  }
                  required
                />
              </label>
            </div>

            <button
              type="button"
              onClick={() => removeQuestion(qIndex)}
              style={{ marginTop: 10 }}
            >
              🗑 Удалить вопрос
            </button>
          </div>
        ))}

        <button type="button" onClick={addQuestion} style={{ marginTop: 20 }}>
          ➕ Добавить вопрос
        </button>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <div style={{ marginTop: 20 }}>
          <button type="submit" disabled={loading}>
            {loading ? "Создание..." : "Создать опрос"}
          </button>
        </div>
      </form>
    </div>
  );
}
