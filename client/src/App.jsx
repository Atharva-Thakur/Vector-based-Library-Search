import React from "react";
import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom";
import Home from "./components/Home";
import ChatApp from "./components/Starchat.jsx";
import { AuthProvider, useAuth } from "./components/AuthContext";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";

const ProtectedRoute = ({children}) => {
    const {user} = useAuth();
    return user ? children : <Navigate to="/login"/>;
};

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/" element={<Register/>}/>
                    <Route path="/Home" element={<ProtectedRoute><Home/></ProtectedRoute>}/>
                    <Route path="/ChatApp" element={<ProtectedRoute><ChatApp/></ProtectedRoute>}/>
                    <Route path="*" element={<Navigate to="/login"/>}/>
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;
