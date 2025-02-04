import React from 'react'

const SearchResult = ({ results }) => {
    console.log(results)
    return (
        <div>
            <h2 className='!font-medium'>Found 5 results:</h2>
            {/* lists of books and metadata*/}
            {
                results.map(res => {
                    return (
                        <>
                        <h1>{res.title}</h1>
                        <h1>{res.about}</h1>
                        </>
                    )

                })
            }
        </div>
    )
}

export default SearchResult
