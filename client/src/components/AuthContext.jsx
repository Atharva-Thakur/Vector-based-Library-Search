import { createContext, useContext, useEffect, useState } from "react";
import axios from "axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = async (email, password) => {
  try {
    const { data } = await axios.post("http://127.0.0.1:8000/account/login/",
      { email, password },
      { withCredentials: true }
    );

    // Store full user data in localStorage
    localStorage.setItem("user", JSON.stringify({
      id: data.id,
      username: data.username,
      email: data.email,
      grade: data.grade,  // Store grade
      token: data.access_token
    }));

    setUser({
      id: data.id,
      username: data.username,
      email: data.email,
      grade: data.grade,
      token: data.access_token
    });

  } catch (error) {
    console.error("Login failed:", error.response?.data?.error);
  }
};


  const register = async (username, email, password, grade) => {
    try {
      await axios.post("http://127.0.0.1:8000/account/register/", { username, email, password, grade }, { withCredentials: true });
    } catch (error) {
      console.error("Registration failed:", error.response?.data);
    }
  };

  const logout = async () => {
    try {
      await axios.get("http://127.0.0.1:8000/account/logout/", { withCredentials: true });
      localStorage.removeItem("user");
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error.response?.data);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
