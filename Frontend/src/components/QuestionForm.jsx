
import { useState } from 'react'
import axios from 'axios'

const QuestionForm = () => {
    const [question, setQuestion] = useState('')
    const [answer, setAnswer] = useState('')

    const api = axios.create({
        baseURL: 'https://localhost:5001/api'
    })

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Your question: ", question);
        const response = await api.post('/chat', { message: question });
        setAnswer(response.data.answer);

    }

    return (
        <div>
            <form>
                <input type='text' value={question} onChange={(e) => setQuestion(e.target.value)} />
                <buton type="submit" ClassName='button' onclick={handleSubmit}>Submit</buton>
            </form>
            <div>
                <h2>Answer:</h2>
                <p>{answer}</p>
            </div>
        </div>
    )
}

export default QuestionForm