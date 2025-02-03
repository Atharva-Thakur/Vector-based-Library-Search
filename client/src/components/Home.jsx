import React from 'react'
import Navbar from './Navbar'
import SearchResult from './SearchResult'

const Home = () => {
    return (
        <>
            <Navbar />
            <div className='flex flex-col items-center justify-center my-12 mx-12'>

                <p className='text-3xl'>
                    AI-Powered Library Search
                </p>

                <div className='relative'>
                    <input type="text" placeholder='Search for books, authors, genres, etc.' className='w-[90vw] sm:w-[75vw] h-14 focus:outline-none border border-gray-600 my-7 p-4 rounded-3xl' />
                    <button className='absolute right-0 top-1/2 -translate-y-1/2 bg-gray-900 text-white h-14 px-8 rounded-r-3xl cursor-pointer'>Search</button>
                </div>

                <SearchResult />
            </div>
        </>
    )
}

export default Home
