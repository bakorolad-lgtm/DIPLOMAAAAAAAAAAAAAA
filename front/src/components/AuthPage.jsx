import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function AuthPage() {
  const [mode, setMode] = useState("login"); // "login" или "register"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { signIn, signUp } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (mode === "login") {
        await signIn(username, password);
      } else {
        await signUp(username, password);
      }
      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Ошибка авторизации или регистрации");
    }
  };

  return (
    <div >
      <h2>{mode === "login" ? "Вход" : "Регистрация"}</h2>

      <div style={{ marginBottom: 20 }}>
        <button
          onClick={() => setMode("login")}
          disabled={mode === "login"}
          style={{ marginRight: 10 }}
        >
          Вход
        </button>
        <button onClick={() => setMode("register")} disabled={mode === "register"}>
          Регистрация
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div>
          <input
            placeholder="Имя пользователя"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            placeholder="Пароль"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">
          {mode === "login" ? "Войти" : "Зарегистрироваться"}
        </button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
    </div>
  );
}
