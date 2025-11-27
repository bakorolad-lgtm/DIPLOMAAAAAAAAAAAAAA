// Updated Courses list and CoursePage components
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getCourses, deleteCourse } from "../api";
import { useAuth } from "../context/AuthContext";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [courseToDelete, setCourseToDelete] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const { role } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    getCourses().then(setCourses);
  }, []);

  const handleDeleteClick = (course) => {
    setCourseToDelete(course);
    setShowModal(true);
  };

  const confirmDelete = async () => {
    if (!courseToDelete) return;
    try {
      await deleteCourse(courseToDelete.id);
      setCourses((prev) => prev.filter((c) => c.id !== courseToDelete.id));
    } catch (err) {
      console.error("Ошибка при удалении:", err);
      alert("Не удалось удалить курс");
    } finally {
      setShowModal(false);
      setCourseToDelete(null);
    }
  };

  const cancelDelete = () => {
    setShowModal(false);
    setCourseToDelete(null);
  };

  return (
    <div>
      <h2>Курсы</h2>

      {role === "admin" && (
        <button type="button" onClick={() => navigate("/courses/new")}>
          Создать
        </button>
      )}

      {courses.length === 0 && <p>Нет курсов</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {courses.map((c) => (
          <li
            key={c.id}
            style={{
              margin: "10px 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              border: "1px solid #ccc",
              borderRadius: "6px",
              padding: "8px 12px",
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
            }}
          >
            <div>
              <Link
                to={`/course/${c.id}`}
                style={{ fontWeight: "bold", textDecoration: "none", color: "black" }}
              >
                {c.title}
              </Link>
            </div>

            {role === "admin" && (
              <button
                type="button"
                onClick={() => handleDeleteClick(c)}
                style={{
                  marginLeft: 10,
                  backgroundColor: "#ff5b5b",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  padding: "4px 8px",
                  cursor: "pointer",
                  whiteSpace: "nowrap",
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
            <h4>Удалить курс?</h4>
            <p>
              Вы уверены, что хотите удалить
              <br />
              <strong>{courseToDelete?.title}</strong>?
            </p>
            <div
              style={{
                marginTop: 15,
                display: "flex",
                gap: 10,
                justifyContent: "center",
              }}
            >
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
