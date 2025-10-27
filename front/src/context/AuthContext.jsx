import { createContext, useContext, useEffect, useState } from "react";
import { login, register } from "../api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [user, setUser] = useState(localStorage.getItem("user") || null);

  useEffect(() => {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }, [token]);

  useEffect(() => {
    if (user) localStorage.setItem("user", user);
    else localStorage.removeItem("user");
  }, [user]);

  const signIn = async (username, password) => {
    const data = await login(username, password);
    console.log(data)
    setToken(`${data.token}`);
    setUser(username);
  };

  const signUp = async (username, password) => {
    const data = await register(username, password);
    setToken(`Bearer ${data.access_token}`);
    setUser(username);
  };

  const signOut = () => {
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
