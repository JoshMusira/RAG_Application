
import { useState } from 'react';
import axios from 'axios';
import { BounceLoader } from 'react-spinners';
import ReactMarkdown from 'react-markdown';
import Expander from './Expander';

const CombinedConversattion = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [keywords, setKeywords] = useState([]);
    const [documents, setDocuments] = useState([]);
    const [wordCloudImage, setWordCloudImage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const api = axios.create({
        baseURL: 'http://127.0.0.1:8000/api'
    });

    const handleSubmit = async (e) => {
        setAnswer('');
        setKeywords([]);
        setIsLoading(true);
        e.preventDefault();
        console.log("Your question: ", question);
        const response = await api.post('/chat-combined', { message: question });
        setAnswer(response.data.answer);
        setKeywords(response.data.keywords);
        setDocuments(response.data.documents);
        setWordCloudImage(response.data.word_cloud_image);
        setIsLoading(false);
    };

    return (
        <div className='main-container'>
            <form className='form'>
                <input type='text' className='form-input' placeholder='Ask your question ...' value={question} onChange={(e) => setQuestion(e.target.value)} />
                <button type="submit" className='text-2xl font-semibold p-[10px] bg-blue-800 rounded-lg cursor-pointer hover:bg-blue-400 border border-blue-500' onClick={handleSubmit}>Submit</button>
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
                        {wordCloudImage && (
                            <div className="results-word-cloud">
                                <h2 className='font-bold text-2xl text-red-500 mt-2'>Word Cloud:</h2>
                                <img src={`data:image/png;base64,${wordCloudImage}`} alt="Word Cloud" />
                            </div>
                        )}
                        {keywords.length > 0 && (
                            <div className="results-keywords">
                                <h2 className='font-bold text-2xl text-red-500 mt-2'>Keywords:</h2>
                                <ul>
                                    {keywords.map((keyword, index) => (
                                        <li key={index}>{keyword}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                    <div className="results-documents">
                        <h2 className='font-bold text-2xl text-red-500'>Documents:</h2>
                        <ul>
                            {documents.map((document, index) => (
                                <Expander key={index} title={document.page_content.split(" ").slice(0, 5).join(" ") + "..."} content={document.page_content} source={document.metadata.source_url} />
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CombinedConversattion;
