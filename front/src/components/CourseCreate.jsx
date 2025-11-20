import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCourse } from "../api";

export default function CreateCoursePage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [blocks, setBlocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function addBlock(type) {
    setBlocks([...blocks, { id: Date.now(), type, content: "" }]);
  }

  function updateBlock(id, value, newType) {
    setBlocks(blocks.map(b => b.id === id ? { ...b, content: value, type: newType || b.type } : b));
  }

  function removeBlock(id) {
    setBlocks(blocks.filter(b => b.id !== id));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const newCourse = await createCourse({
        title,
        blocks
      });
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

        <h3>Текст курса</h3>
        {blocks.map(block => (
          <div key={block.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
            <select value={block.type} onChange={e => updateBlock(block.id, block.content, e.target.value)}>
              <option value="text">Текст</option>
              <option value="image">Изображение</option>
              <option value="video">Видео</option>
            </select>
            {block.type === "text" && (
              <textarea
                value={block.content}
                onChange={e => updateBlock(block.id, e.target.value)}
                placeholder="Введите текст"
              />
            )}
            {block.type === "image" && (
              <input
                type="file"
                accept="image/*"
                onChange={e => updateBlock(block.id, e.target.files[0])}
              />
            )}
            {block.type === "video" && (
              <input
                type="file"
                accept="video/*"
                onChange={e => updateBlock(block.id, e.target.files[0])}
              />
            )}
            <button type="button" onClick={() => removeBlock(block.id)}>Удалить</button>
          </div>
        ))}

        <div>
          <button type="button" onClick={() => addBlock("text")} style={{marginBottom:10}}>Добавить</button>
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={loading || blocks.length === 0 || blocks.some(b => !b.content || (typeof b.content === "string" && b.content.trim() === ""))}>
          {loading ? "Создание..." : "Создать"}
        </button>
      </form>
    </div>
  );
}
