import React from 'react'
import link from '../assets/link.svg'
const SearchResult = ({ results }) => {
    return (
        <div className='min-h-screen'>
            {
                results.length > 0 &&
                <h2 className='!font-medium'>Found {results.length} results:</h2>
            }
            {/* lists of books and metadata*/}
            <div className='grid grid-cols-1 sm:grid-cols-2 gap-4 my-4'>

                {
                    results.map(res => {
                        return (
                            <div key={res.id} className='bg-slate-50 p-4 rounded-xl border border-slate-400'>
                                <div className="flex items-center gap-2">
                                    <h1 className='!font-semibold line-clamp-1'>
                                        {res.title}
                                    </h1>
                                    <a href={res.link} className='shrink-0'>
                                        <img src={link} alt="link" />
                                    </a>
                                </div>
                                <p className='italic text-gray-600'>{res.author} | {res.year}</p>
                                <ul className='flex flex-wrap gap-1 my-1'>
                                    {
                                        JSON.parse(res.genre.replace(/'/g, '"')).map(g => {
                                            return (
                                                <li className='bg-slate-200 px-2 py-1 rounded-lg text-xs'>{g}</li>
                                            )
                                        })
                                    }
                                </ul>
                                <h1 className='line-clamp-5 mt-2 leading-5'>{res.about}</h1>
                            </div>
                        )

                    })
                }
            </div>
        </div>
    )
}

export default SearchResult
