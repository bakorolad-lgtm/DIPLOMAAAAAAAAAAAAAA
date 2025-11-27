import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createQuiz } from "../api";

export default function CreateQuizPage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [questions, setQuestions] = useState([
    { id: 1, title: "", answers: [""], correct_answer: "" },
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

    // если удалили/изменили правильный ответ — сбросим его
    const currentCorrect = updated[qIndex].correct_answer;
    if (currentCorrect && !updated[qIndex].answers.includes(currentCorrect)) {
      updated[qIndex].correct_answer = "";
    }

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
              maxLength={120}
              required
            />
          </label>
        </div>

        {questions.map((q, qIndex) => (
          <div
            key={q.id}
            style={{
              border: "1px solid #ccc",
              padding: 10,
              marginTop: 15,
              borderRadius: 8,
            }}
          >
            <h4>Вопрос #{q.id}</h4>

            <label>
              Текст вопроса:
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
                <div key={aIndex} style={{ marginTop: 5 }}>
                  <input
                    type="text"
                    value={a}
                    placeholder={`Ответ ${aIndex + 1}`}
                    onChange={(e) =>
                      handleAnswerChange(qIndex, aIndex, e.target.value)
                    }
                    required
                  />

                  <label style={{ marginLeft: 10 }}>
                    <input
                      type="radio"
                      name={`correct_${q.id}`}
                      value={a}
                      checked={q.correct_answer === a}
                      onChange={() =>
                        handleQuestionChange(qIndex, "correct_answer", a)
                      }
                      disabled={!a.trim()}
                    />
                    Правильный
                  </label>
                </div>
              ))}

              <button
                type="button"
                onClick={() => addAnswer(qIndex)}
                style={{ marginTop: 10 }}
              >
                ➕ Добавить ответ
              </button>
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
