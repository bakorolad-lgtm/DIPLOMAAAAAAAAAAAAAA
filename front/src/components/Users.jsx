import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getUsers } from "../api";

export default function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    getUsers().then(setUsers);
  }, []);

  return (
    <div>
      <h2>Пользователи</h2>
      {users.length === 0 && <p>Нет пользователей</p>}
      <ul>
        {users.map((user, i) => (
          <li key={i} style={{ marginBottom: "10px" }}>
            <Link to={`/quiz/user/answers/${user.id || i}`} style={{ fontWeight: "bold" }}>
              {user.email}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
