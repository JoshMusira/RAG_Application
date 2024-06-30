import axios from 'axios';
import React, { useState } from 'react';
import { BounceLoader } from 'react-spinners';
import ReactMarkdown from 'react-markdown';

const Home = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const api = axios.create({
        baseURL: 'http://127.0.0.1:8000/api'
    });

    const handleSubmit = async (e) => {
        setAnswer('');
        setIsLoading(true);
        e.preventDefault();
        console.log("Your question: ", question);

        try {
            const response = await api.post('/indexing', { message: question });
            const data = response.data;

            // Ensure response is string before setting answer
            const responseText = typeof data.response === 'string' ? data.response : JSON.stringify(data.response);
            setAnswer(responseText);
        } catch (error) {
            console.error('Error indexing:', error);
            setAnswer('An error occurred while indexing the URL.');
        }

        setIsLoading(false);
    };

    // console.log(answer);

    return (
        <div className='main-container'>
            <form className='w-[90%] flex gap-10' onSubmit={handleSubmit}>
                <input
                    type='text'
                    className='form-input-home'
                    required
                    placeholder='Paste your website URL to  for retrieval ...'
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button
                    type="submit"
                    className='text-2xl w-[20%] font-semibold p-[10px] bg-pink-800 rounded-lg cursor-pointer hover:bg-pink-400 border border-pink-500'
                >
                    Add to database
                </button>
            </form>

            {isLoading && (
                <div className="loader-container">
                    <BounceLoader color="#3498db" />
                </div>
            )}

            {answer && (
                <div className="results-container">
                    <div className="results-answer">
                        <h2 className='text-red-600 mb-2'>Response:</h2>
                        <ReactMarkdown>{answer}</ReactMarkdown>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Home;
