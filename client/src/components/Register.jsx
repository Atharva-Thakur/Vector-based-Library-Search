import { useState } from "react";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [grade, setGrade] = useState(0);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await register(username, email, password, grade);
    navigate("/login"); // Redirect after registration
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl mb-4">Register</h2>
      <form onSubmit={handleSubmit}>
        <input className="w-full p-2 mb-2 border" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className="w-full p-2 mb-2 border" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full p-2 mb-2 border" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <input className="w-full p-2 mb-2 border" type="number" min="0" max="12" placeholder="Grade" value={grade} onChange={(e) => setGrade(Number(e.target.value))} />
        <button className="w-full bg-green-500 text-white p-2" type="submit">Register</button>
      </form>
      <h2 className="text-xl mt-4 flex justify-end cursor-pointer" onClick={() => {navigate("/login"); }}>Login</h2>
    </div>
  );
};

export default Register;
