import axios from "axios";

const API_URL = "/"; // замени на свой адрес

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Автоматически добавляем токен
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = token;
  return config;
});

// ===== АВТОРИЗАЦИЯ =====
export const login = async (email, password) => {
  const res = await api.post("/auth/login", { email, password });
  return res.data; // ожидается { access_token: "..." }
};

export const register = async (email, password) => {
  const res = await api.post("/auth/register", { email, password });
  return res.data; // ожидается { access_token: "..." }
};

// ===== КУРСЫ =====
export const getCourses = async () => {
  const res = await api.get("/courses");
  return res.data;
};


export const createCourse = async (obj) => {
  const res = await api.post("/courses", obj);
  return res.data;
}


export const deleteCourse = async (course_id) => {
  await api.delete(`/courses/${course_id}`);
}


export const deleteQuiz = async (quiz_id) => {
  await api.delete(`/quiz/${quiz_id}`);
}


export const getCourse = async (course_id) => {
  const res = await api.get(`/courses/${course_id}`);
  return res.data;
};


export const getUsers = async () => {
  const res = await api.get(`/auth`);
  return res.data;
};

// ===== ТЕСТЫ =====

export const createQuiz = async (obj) => {
  const res = await api.post("/quiz", obj);
  return res.data;
};

export const getQuizzes = async () => {
  const res = await api.get("/quiz");
  return res.data;
};

export const getQuizCheckAnswers = async (quiz_id, user_id) => {
  const params = { quiz_id };
  if (user_id) params.user_id = user_id;
  const res = await api.get("/quiz/check_answers", {
    params,
  });
  return res.data;
};

export const getUserAnswers = async (user_id) => {
  const res = await api.get("/quiz/user/answers", {
    params: { user_id },
  });
  return res.data;
};

export const sendQuizAnswers = async (quiz_id, answers) => {
  const res = await api.post("/quiz/answer", { quiz_id, answers });
  return res.data;
};
