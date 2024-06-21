
import { useState } from 'react'
import axios from 'axios'
import { BounceLoader } from 'react-spinners';
import ReactMarkdown from 'react-markdown';
import Expander from './Expander';

const QuestionForm = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [documents, setDocuments] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const api = axios.create({
        baseURL: 'http://127.0.0.1:8000/api'
    })

    const handleSubmit = async (e) => {
        setAnswer('');
        setIsLoading(true);
        e.preventDefault();
        console.log("Your question: ", question);
        const response = await api.post('/chat', { message: question });
        setAnswer(response.data.answer);
        setDocuments(response.data.documents)
        setIsLoading(false);
    }

    return (
        <div className='main-container'>
            <form className='form'>
                <input type='text' className='form-input' value={question} onChange={(e) => setQuestion(e.target.value)} />
                <button type="submit" className='text-2xl font-semibold p-[10px] bg-blue-800 rounded-lg cursor-pointer hover:bg-blue-400 border border-blue-500' onClick={handleSubmit}>Submit</button >
            </form>

            {isLoading && (
                <div className="loader-container">
                    <BounceLoader color="#3498db" />
                </div>
            )}
            {answer && (
                <div className="results-container">
                    <div className="results-answer">
                        <h2 className='font-bold text-2xl text-red-500 mb-3'>Answer:</h2>
                        <ReactMarkdown>{answer}</ReactMarkdown>
                    </div>
                    <div className="results-documents">
                        <h2 className='font-bold text-2xl text-red-500'>Documents:</h2>
                        <ul>
                            {documents.map((documents, index) => (
                                <Expander key={index} title={documents.page_content.split(" ").slice(0, 5).join(" ") + "..."} content={documents.page_content} source={documents.metadata.source_url} />
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    )
}

export default QuestionForm