import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getQuizzes, deleteQuiz } from "../api";
import { useAuth } from "../context/AuthContext";

export default function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const [quizToDelete, setQuizToDelete] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const { role } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    getQuizzes().then(setQuizzes);
  }, []);

  const handleDeleteClick = (quiz) => {
    setQuizToDelete(quiz);
    setShowModal(true);
  };

  const confirmDelete = async () => {
    if (!quizToDelete) return;
    try {
      await deleteQuiz(quizToDelete.id);
      setQuizzes((prev) => prev.filter((q) => q.id !== quizToDelete.id));
    } catch (err) {
      console.error("Ошибка при удалении:", err);
      alert("Не удалось удалить тест");
    } finally {
      setShowModal(false);
      setQuizToDelete(null);
    }
  };

  const cancelDelete = () => {
    setShowModal(false);
    setQuizToDelete(null);
  };

  return (
    <div>
      <h2>Тесты</h2>

      {role === "admin" && (
        <button type="button" onClick={() => navigate("/quiz/new")}>
          Создать
        </button>
      )}
      {users.length === 0 && <p>Нет тестов</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {quizzes.map((q) => (
          <li
            key={q.id}
            style={{
              margin: "8px 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              border: "1px solid #ccc",
              borderRadius: "6px",
              padding: "8px 12px",
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)"
            }}
          >
            <Link to={`/quiz/${q.id}`} style={{ textDecoration: "none" }}>
              {q.title}
            </Link>

            {role === "admin" && (
              <button
                type="button"
                onClick={() => handleDeleteClick(q)}
                style={{
                  marginLeft: 10,
                  backgroundColor: "#ff5b5b",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  padding: "4px 8px",
                  cursor: "pointer",
                }}
              >
                Удалить
              </button>
            )}
          </li>
        ))}
      </ul>

      {showModal && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0,0,0,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: 20,
              borderRadius: 8,
              width: "300px",
              textAlign: "center",
            }}
          >
            <h4>Удалить тест?</h4>
            <p>
              Вы уверены, что хотите удалить
              <br />
              <strong>{quizToDelete?.title}</strong>?
            </p>
            <div style={{ marginTop: 15, display: "flex", gap: 10, justifyContent: "center" }}>
              <button
                onClick={confirmDelete}
                style={{
                  backgroundColor: "#ff5b5b",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  padding: "6px 12px",
                  cursor: "pointer",
                }}
              >
                Да, удалить
              </button>
              <button
                onClick={cancelDelete}
                style={{
                  backgroundColor: "#ccc",
                  border: "none",
                  borderRadius: 4,
                  padding: "6px 12px",
                  cursor: "pointer",
                }}
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
