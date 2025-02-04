import React, { useState } from 'react'
import Navbar from './Navbar'
import SearchResult from './SearchResult'
import axios from 'axios'

const Home = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);


    const handleSubmit = async () => {
        const { data } = await axios.post('https://studious-invention-x776g55wpvjh9vpx-8000.app.github.dev/search', { query });
        console.log(data);
        setResults(data?.results)
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

                <div className='relative'>
                    <input value={query} onChange={(event) => handleChange(event)} type="text" placeholder='Search for books, authors, genres, etc.' className='w-[90vw] sm:w-[75vw] h-14 focus:outline-none border border-gray-600 my-7 p-4 rounded-3xl' />
                    <button onClick={handleSubmit} className='absolute right-0 top-1/2 -translate-y-1/2 bg-gray-900 text-white h-14 px-8 rounded-r-3xl cursor-pointer'>Search</button>
                </div>

                <SearchResult results={results} />
            </div>
        </>
    )
}

export default Home
