import React from 'react'

const Navbar = () => {
    return (
        <nav className='flex justify-between px-4 sm:px-14 py-4 border-b-2 border-gray-100 sticky top-0 bg-white z-50'>
            <h1 className='text-xl text-gray-900 !font-medium cursor-pointer'>Lib.ai</h1>

            <ul className='flex items-center space-x-4'>
                <li className='cursor-no-drop'>Home</li>
                <li className='cursor-no-drop'>Explore</li>
                <li className='cursor-no-drop'>About</li>
            </ul>

        </nav>
    )
}

export default Navbar
