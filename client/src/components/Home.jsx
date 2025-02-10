import React, { useState } from 'react'
import Navbar from './Navbar'
import SearchResult from './SearchResult'
import axios from 'axios'
import book from '../assets/Book.gif'

const Home = () => {
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [results, setResults] = useState([]);


    const handleSubmit = async (e) => {
        e.preventDefault();
        if (query.length === 0) return;
        setIsLoading(true)
        // const { data } = await axios.post('https://sturdy-space-lamp-p44v5jjrwxgcgr7-8000.app.github.dev/search', { query });
        const { data } = await axios.post('http://localhost:8001/search', { query });
        console.log(data);
        setResults(data?.results)
        setIsLoading(false)
    }

    const handleChange = (event) => {
        setQuery(event.target.value);
    }

    return (
        <>
            <Navbar />
            <div className='flex flex-col items-center justify-center my-12 mx-12'>

                <p className='text-3xl'>
                    AI-Powered Library Search
                </p>

                <form className='relative' onSubmit={(e) => handleSubmit(e)}>
                    <input value={query} onChange={(event) => handleChange(event)} type="text" placeholder='Search for books, authors, genres, etc.' className='w-[90vw] sm:w-[70vw] h-14 focus:outline-none border border-gray-600 my-7 p-4 rounded-3xl' />
                    <button className='absolute right-0 top-1/2 -translate-y-1/2 bg-gray-900 text-white h-14 px-8 rounded-r-3xl cursor-pointer'>Search</button>
                </form>

                {
                    isLoading ?
                        <div className='flex items-center justify-center flex-col gap-2 mt-4'>
                            <img src={book} alt="loading" className='w-10' />
                            <h2 className='italic'>Hang tight! We're fetching your books... ⏳</h2>
                        </div> :
                        <SearchResult results={results} />
                }
            </div>
        </>
    )
}

export default Home
