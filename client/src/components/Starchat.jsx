import React, {useState} from 'react';
import axios from "axios";
import Navbar from "./Navbar.jsx";
import {useAuth} from "./AuthContext.jsx";

export default function ChatApp() {
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState('');
    const [document, setDocument] = useState(null);
    const [response, setResponse] = useState('');
    const [loader, setloader] = useState(false);
    const { user } = useAuth();


    const handleSubmit = async (e) => {
        e.preventDefault();
        setloader(true);
        if (!currentQuestion.trim()) return;
        const formData = new FormData();
        formData.append('question', currentQuestion);
        formData.append('grade', user?.grade);
        if (document) {
            formData.append('document', document);
        }
        try {
            // Send the question to the Django backend
            const response = await axios.post('http://localhost:8000/LLM/llm_chat/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Update the state with the received response
            setResponse(response.data.answer);

            // Append the current question and its response to the list of questions
            setQuestions(prevQuestions => [...prevQuestions, {
                question: currentQuestion,
                answer: response.data.answer
            }]);

            // Clear the input field
            setCurrentQuestion('');
            setloader(false);
        } catch (error) {
            setloader(false);
            console.error('Error:', error);
        }
    };

    const handleChange = (event) => {
        setCurrentQuestion(event.target.value);
    };

    const convertWhitespaceToHTML = (text) => {
        return text.split('\n').map((item, index) => (
            <span key={index}>
        {item}
                <br/>
      </span>
        ));
    };

    return (
        <form onSubmit={handleSubmit} className={"w-full h-screen overflow-hidden bg-white text-black"}>
            <Navbar />
            <div className="w-full h-full p-4">
                <div className="w-full h-full relative">
                    <div className="absolute rounded-3xl w-full h-full overflow-hidden">
                        <div className={"rounded-3xl w-full h-full blur-sm "}></div>
                    </div>
                    <div className="absolute z-10 w-full h-full">
                        <div className="w-full h-full">
                            <div className="w-full h-full pb-36 overflow-y-auto">
                                {loader ? (
                                    <div className="w-full h-full animate-pulse">
                                        <div className="w-full h-full grid grid-rows-5 gap-4 px-12 py-12">
                                            <div className="w-full h-full grid grid-cols-6 gap-4">
                                                <div
                                                    className="w-full h-full flex items-center justify-center col-span-5">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                                <div className="w-full h-full flex items-center justify-center">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                            </div>
                                            <div className="w-full h-full grid grid-cols-6 gap-4">
                                                <div className="w-full h-full flex items-center justify-center">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                                <div
                                                    className="w-full h-full flex items-center justify-center col-span-5">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                            </div>
                                            <div className="w-full h-full grid grid-cols-6 gap-4">
                                                <div
                                                    className="w-full h-full flex items-center justify-center col-span-5">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                                <div className="w-full h-full flex items-center justify-center">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                            </div>
                                            <div className="w-full h-full grid grid-cols-6 gap-4">
                                                <div
                                                    className="w-full h-full flex items-center justify-center col-span-5">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                                <div className="w-full h-full flex items-center justify-center">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                            </div>
                                            <div className="w-full h-full grid grid-cols-6 gap-4">
                                                <div className="w-full h-full flex items-center justify-center">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                                <div
                                                    className="w-full h-full flex items-center justify-center col-span-5">
                                                    <div className="w-full h-4 bg-slate-500 rounded-full"></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ) : (<div>{questions.map((item, index) => (
                                    <div key={index} className="w-full h-full px-10 pt-10">
                                        <div
                                            className={"w-full h-full backdrop-blur-lg bg-opacity-20 p-4 rounded-3xl grid grid-cols-12 mb-10 bg-white"}>
                                            <div className="w-full h-full">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                                     stroke-width="1.5" stroke="currentColor" className="size-8">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
                                                </svg>
                                            </div>
                                            <div
                                                className="w-full h-full col-span-11">{convertWhitespaceToHTML(item.question)}</div>
                                        </div>
                                        <div
                                            className={"w-full h-full  backdrop-blur-lg bg-opacity-20 p-4 rounded-3xl grid grid-cols-12 bg-white"}>
                                            <div className="w-full h-full">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                                     stroke-width="1.5" stroke="currentColor" className="size-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z"/>
                                                </svg>
                                            </div>
                                            <div
                                                className="w-full h-full col-span-11">{convertWhitespaceToHTML(item.answer)}</div>
                                        </div>
                                    </div>
                                ))}</div>)}
                            </div>
                        </div>
                    </div>
                    <div className="absolute z-20 w-full h-1/6 flex items-center justify-center bottom-10">
                        <div className="w-3/4 h-3/4 relative">
                <textarea
                    className={"bg-white w-full h-full pt-4 pl-6 pr-10 rounded-3xl z-20 absolute bottom-0 overflow-y-auto backdrop-blur-lg bg-opacity-20 resize-none border-2 focus:outline-none border-solid border-black text-black"}
                    value={currentQuestion}
                    onChange={handleChange}
                    placeholder="Enter Message...."

                />
                            <button disabled={loader} type="submit"
                                    className="w-10 h-10 cursor-pointer border border-black flex items-center justify-center bg-white rounded-xl right-4 bottom-1/4 absolute z-20">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                     stroke-width="1.5" stroke="currentColor"
                                     className="w-6 h-6 text-black animate-pulse">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                          d="m4.5 18.75 7.5-7.5 7.5 7.5"/>
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                          d="m4.5 12.75 7.5-7.5 7.5 7.5"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    );
}
