import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BounceLoader } from 'react-spinners';

const ImageDisplay = () => {
    const [images, setImages] = useState({
        source_url_image: '',
        sentiment_polarity_image: '',
        topic_frequencies_img: '',
        stacked_image: '',
        sentiment_polarity_img_per_domain: {}
    });
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
        <div className='main-container p-4'>
            {loading ? (
                <div className="flex justify-center items-center h-screen">
                    <BounceLoader color="#3498db" />
                </div>
            ) : (
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                    <div>
                        <h1 className='pb-3 text-2xl text-blue-700 font-bold py-2'>Source URL Distribution</h1>
                        {images.source_url_image && <img src={`data:image/png;base64,${images.source_url_image}`} alt="Source URL Distribution" />}
                    </div>
                    <div>
                        <h1 className='pb-3 text-2xl text-blue-700 font-bold py-2'>Overal Sentiment Polarity Distribution</h1>
                        {images.sentiment_polarity_image && <img src={`data:image/png;base64,${images.sentiment_polarity_image}`} alt="Sentiment Polarity Distribution" />}
                    </div>
                    <div>
                        <h1 className='pb-3 text-2xl text-blue-700 font-bold py-2'>Most Addressed Topics in the Articles</h1>
                        {images.topic_frequencies_img && <img src={`data:image/png;base64,${images.topic_frequencies_img}`} alt="Topic Frequencies Distribution" />}
                    </div>
                    <div>
                        <h1 className='pb-3 text-2xl text-blue-700 font-bold py-2'>Distribution of Topics Covered by Each News Source</h1>
                        {images.stacked_image && <img src={`data:image/png;base64,${images.stacked_image}`} alt="Stacked Bar Distribution" />}
                    </div>
                    {Object.keys(images.sentiment_polarity_img_per_domain).map((domain, index) => (
                        <div key={index}>
                            <h1 className='pb-3 text-2xl text-blue-700 font-bold py-2'>Sentiment Polarity for {domain}</h1>
                            {images.sentiment_polarity_img_per_domain[domain] &&
                                <img src={`data:image/png;base64,${images.sentiment_polarity_img_per_domain[domain]}`} alt={`Sentiment Polarity for ${domain}`} />}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ImageDisplay;
