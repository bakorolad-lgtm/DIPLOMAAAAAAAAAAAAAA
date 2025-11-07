import { createContext, useContext, useEffect, useState } from "react";
import { login, register } from "../api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [user, setUser] = useState(localStorage.getItem("user") || null);
  const [role, setRole] = useState(localStorage.getItem("role") || null);

  useEffect(() => {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }, [token]);

  useEffect(() => {
    if (user) localStorage.setItem("user", user);
    else localStorage.removeItem("user");
  }, [user]);

  useEffect(() => {
    if (role) localStorage.setItem("role", role);
    else localStorage.removeItem("role");
  }, [role]);

  const signIn = async (username, password) => {
    console.log("Signin")
    const data = await login(username, password);
    setToken(`${data.token}`);
    setUser(username);
    setRole(data.role);
  };

  const signUp = async (username, password) => {
    console.log("Signup")
    const data = await register(username, password);
    setToken(`Bearer ${data.access_token}`);
    setUser(username);
    setRole(data.role);
  };

  const signOut = () => {
    console.log("signOut");
    setToken(null);
    setUser(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, role, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
