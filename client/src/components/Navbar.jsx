import React from 'react'
import {useNavigate} from "react-router-dom";
import {useAuth} from "./AuthContext.jsx";

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    return (
        <nav className='flex justify-between px-4 sm:px-14 py-4 border-b-2 border-gray-100 sticky top-0 bg-white z-50'>
            {user ?<h1 className='text-xl text-gray-900 !font-medium cursor-pointer'>Welcome, {user.username}</h1> : <h1 className='text-xl text-gray-900 !font-medium cursor-pointer'>Lib.ai</h1>}


            <ul className='flex items-center space-x-4'>
                <li className='cursor-pointer' onClick={()=>{
                    navigate('/Home');
                }}>Home</li>
                <li className='cursor-no-drop'>Explore</li>
                <li className='cursor-pointer' onClick={() => {navigate("/"); }}>Register</li>
                {user ? <li className='cursor-pointer text-red-500' onClick={() => { logout(); navigate("/login"); }}>Log out</li> : <li className='cursor-pointer' onClick={() => { navigate("/login"); }}>Login</li>}
            </ul>

        </nav>
    )
}

export default Navbar
