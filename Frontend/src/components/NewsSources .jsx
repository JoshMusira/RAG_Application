import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NewsSources = () => {
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const api = axios.create({
        baseURL: 'http://127.0.0.1:8000/api'
    });

    useEffect(() => {
        const fetchSources = async () => {
            try {
                const response = await api.get('/news-sources');
                setSources(response.data.sources);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchSources();
    }, []);

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;
    if (error) return <div className="flex justify-center items-center h-screen text-red-500">Error: {error}</div>;

    return (
        <div className="min-h-screen  flex items-center justify-center pb-10 px-4">
            <div className=" shadow-lg rounded-lg p-6 w-full max-w-5xl">
                <h1 className="text-3xl font-bold mb-6 text-center">News Sources</h1>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                    {sources.map((source) => (
                        <div key={source} className="p-4 bg-gray-50 text-black rounded-lg shadow-sm hover:bg-gray-100 transition duration-200">
                            {source}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default NewsSources;
