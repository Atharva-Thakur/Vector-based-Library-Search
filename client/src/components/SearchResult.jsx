import React from 'react'
import link from '../assets/link.svg'
import axios from "axios";
import {useNavigate} from "react-router-dom";

const SearchResult = ({results}) => {
    const navigate = useNavigate();
    const toggleTitle = async (title) => {
        try {
            await axios.post("http://localhost:8000/LLM/update-title/", {title: title});
            navigate('/chatapp');
        } catch (error) {
            console.error("Failed to update title in backend", error);
        }
    };
    return (
        <div className='min-h-screen mx-6 sm:mx-24'>
            {
                results.length > 0 &&
                <h2 className='!font-medium'>Found {results.length + 2} results:</h2>
            }
            {/* lists of books and metadata*/}
            <div className='grid grid-cols-1 gap-4 my-4'>
                {
                    results.length > 0 &&
                    <>
                        <div onClick={()=>toggleTitle('An Introduction to Mechanical Engineering')}
                             className='bg-slate-50 cursor-pointer p-4 rounded-xl border border-slate-400'>
                            <div className="flex items-center gap-2">
                                <h1 className='!font-semibold line-clamp-1'>
                                    An Introduction to Mechanical Engineering Grade-12
                                </h1>
                                <a className='shrink-0'>
                                    <img src={link} alt="link"/>
                                </a>
                            </div>
                            <p className='italic text-gray-600'>Jonathan Wickert | 2018</p>
                            <ul className='flex flex-wrap gap-1 my-1'>
                                <li className='bg-slate-200 px-2 py-1 rounded-lg text-xs'>Education</li>
                            </ul>
                            <h1 className='line-clamp-5 mt-2 leading-5'>An Introduction to Mechanical Engineering is a
                                foundational textbook that provides a comprehensive overview of the principles,
                                applications, and fundamental concepts of mechanical engineering and its connection to
                                science. Covering topics such as thermodynamics, fluid mechanics, materials science, and
                                machine design, the book serves as an essential resource for students and professionals
                                looking to build a strong understanding of the field. With real-world examples,
                                problem-solving techniques, and engineering case studies, it bridges theoretical
                                knowledge with practical applications, making it an ideal starting point for those
                                pursuing a career in mechanical engineering.</h1>
                        </div>
                        <div onClick={()=>toggleTitle('science and technology')} className='bg-slate-50 cursor-pointer p-4 rounded-xl border border-slate-400'>
                            <div className="flex items-center gap-2">
                                <h1 className='!font-semibold line-clamp-1'>
                                    Science and Technology Grade-9
                                </h1>
                                <a className='shrink-0'>
                                    <img src={link} alt="link"/>
                                </a>
                            </div>
                            <p className='italic text-gray-600'>John gill | 2016</p>
                            <ul className='flex flex-wrap gap-1 my-1'>
                                <li className='bg-slate-200 px-2 py-1 rounded-lg text-xs'>Education</li>
                            </ul>
                            <h1 className='line-clamp-5 mt-2 leading-5'>Science and Technology is a comprehensive
                                textbook designed to introduce students to key scientific principles and their
                                technological applications. Covering subjects such as physics, chemistry, biology, and
                                environmental science, the book helps students develop a strong foundation in scientific
                                inquiry and critical thinking. With engaging explanations, real-world examples, and
                                hands-on experiments, it connects theoretical concepts to everyday life, fostering
                                curiosity and a deeper understanding of how science and technology shape the modern
                                world.</h1></div>
                    </>
                }
                {
                    results.map(res => {
                        return (
                            <div key={res.id}
                                 className='bg-slate-50 cursor-pointer p-4 rounded-xl border border-slate-400'>
                                <div className="flex items-center gap-2">
                                    <h1 className='!font-semibold line-clamp-1'>
                                        {res.title}
                                    </h1>
                                    <a href={res.link} className='shrink-0'>
                                        <img src={link} alt="link"/>
                                    </a>
                                </div>
                                <p className='italic text-gray-600'>{res.author} | {res.year}</p>
                                <ul className='flex flex-wrap gap-1 my-1'>
                                    {
                                        (() => {
                                            let genres;
                                            try {
                                                genres = JSON.parse(res.genre.replace(/'/g, '"'));
                                                genres = Array.isArray(genres) ? genres : [genres];  // Ensure genres is always an array
                                            } catch {
                                                genres = [res.genre];  // If JSON parsing fails, treat it as a plain string
                                            }
                                            return genres.map((g, index) => (
                                                <li key={index}
                                                    className='bg-slate-200 px-2 py-1 rounded-lg text-xs'>{g}</li>
                                            ));
                                        })()
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
