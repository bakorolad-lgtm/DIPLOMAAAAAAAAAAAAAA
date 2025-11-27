import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getUsers, updateUserRole } from "../api";

export default function Users() {
  const [users, setUsers] = useState([]);
  const [userToAdmin, setUserToAdmin] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    getUsers().then(setUsers);
  }, []);

  const confirmMakeAdmin = async () => {
      if (!userToAdmin) return;
      try {
        await updateUserRole(userToAdmin.id, "admin");
        setUsers((prev) => prev.filter((c) => c.id !== userToAdmin.id));
        alert(`Пользователь ${userToAdmin.email} теперь администратор.`);
      } catch (err) {
        console.error("Ошибка при выдаче прав администратора:", err);
        alert("Не удалось выдать права администратора");
      } finally {
        setShowModal(false);
        setUserToAdmin(null);
      }
    };

  const cancelMakeAdmin = () => {
    setShowModal(false);
    setUserToAdmin(null);
  };

  const handleMakeAdmin = (user) => {
    setUserToAdmin(user);
    setShowModal(true);
  };


  return (
    <div>
      <h2>Пользователи</h2>
      {users.length === 0 && <p>Нет пользователей</p>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {users.map((user) => (
          <li
            key={user.id}
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
                to={`/quiz/user/answers/${user.id}`}
                style={{ fontWeight: "bold", textDecoration: "none", color: "#333" }}
              >
                {user.email}
              </Link>
              <div style={{ color: "#555", fontSize: "0.9em" }}>
                Роль: {user.role || "user"}
              </div>
            </div>

            {user.role !== "admin" && (
              <button
                type="button"
                onClick={() => handleMakeAdmin(user)}
                style={{
                  marginLeft: 10,
                  backgroundColor: "#4caf50",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  padding: "6px 10px",
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                }}
              >
                Сделать администратором
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
            <h4>Выдать права администратора??</h4>
            <p>
              Вы уверены, что хотите выдать права администратора
              <br />
              <strong>{userToAdmin?.email}</strong>?
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
                onClick={confirmMakeAdmin}
                style={{
                  backgroundColor: "#4caf50",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  padding: "6px 12px",
                  cursor: "pointer",
                }}
              >
                Да, выдать
              </button>
              <button
                onClick={cancelMakeAdmin}
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
