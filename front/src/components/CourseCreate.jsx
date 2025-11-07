import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCourse } from "../api"; // функция, которая делает POST-запрос

export default function CreateCoursePage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const newCourse = await createCourse({ title, description });
      navigate(`/course/${newCourse.id}`);
    } catch (err) {
      setError("Не удалось создать курс");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2>Создание нового курса</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Название:
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </label>
        </div>

        <div>
          <label>
            Описание:
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </label>
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? "Создание..." : "Создать"}
        </button>
      </form>
    </div>
  );
}
