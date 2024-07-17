import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BounceLoader } from 'react-spinners';

const ImageDisplay = () => {
    const [images, setImages] = useState({ source_url_image: '', sentiment_polarity_image: '', topic_frequencies_img: '' });
    const [loading, setLoading] = useState(true);

    const api = axios.create({
        baseURL: 'http://127.0.0.1:8000/api'
    });

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await api.get('/plots');
                setImages(response.data);
            } catch (error) {
                console.error('Error fetching images:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchImages();
    }, []);

    return (
        <div className='main-container'>
            {loading ? (
                <div className="loader-container">
                    <BounceLoader color="#3498db" />
                </div>
            ) : (
                <>
                    <h1 className=' pb-3 text-2xl text-blue-700 font-bold py-2'>Source URL Distribution</h1>
                    {images.source_url_image && <img src={`data:image/png;base64,${images.source_url_image}`} alt="Source URL Distribution" />}
                    <h1 className=' pb-3 text-2xl text-blue-700 font-bold py-2'>Sentiment Polarity Distribution</h1>
                    {images.sentiment_polarity_image && <img src={`data:image/png;base64,${images.sentiment_polarity_image}`} alt="Sentiment Polarity Distribution" />}
                    <h1 className=' pb-3 text-2xl text-blue-700 font-bold py-2'>Most addresed Topics in the articles</h1>
                    {images.topic_frequencies_img && <img src={`data:image/png;base64,${images.topic_frequencies_img}`} alt="Topic Frequencies Distribution" />}
                </>
            )}
        </div>
    );
};

export default ImageDisplay;
