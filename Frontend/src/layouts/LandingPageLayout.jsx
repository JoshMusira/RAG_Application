import React, { useState } from 'react';
import { Outlet } from "react-router-dom";
import { NavLink } from "react-router-dom";
import axios from 'axios';
import ConfirmURLs from "../components/ConfirmURLs";
import ConfirmModal from '../components/ConfirmModal ';

const LandingPageLayout = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [totalUrls, setTotalUrls] = useState(0);
    const [isTotalUrlsModalOpen, setIsTotalUrlsModalOpen] = useState(false);
    const [isLoadingTotalUrls, setIsLoadingTotalUrls] = useState(false); // Loading state

    const api = axios.create({
        baseURL: 'http://127.0.0.1:8000/api'
    });

    const handleDeleteClick = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handleConfirmDelete = async () => {
        setIsModalOpen(false);
        try {
            const response = await api.post('/delete-collection-content', {
                collectionName: 'Joe Bidens News'
            });
            alert(response.data.message);
        } catch (error) {
            console.log(error);
            alert("There was an error deleting the collection content!", error);
        }
    };

    const handleTotalUrlsClick = async () => {
        setIsLoadingTotalUrls(true); // Set loading state
        try {
            const response = await api.get('/count-unique-urls');
            setTotalUrls(response.data.message);
            setIsTotalUrlsModalOpen(true);
        } catch (error) {
            console.log(error);
            alert("There was an error fetching the total URLs!", error);
        } finally {
            setIsLoadingTotalUrls(false); // Reset loading state
        }
    };
    const handleTotalCombinedUrlsClick = async () => {
        setIsLoadingTotalUrls(true); // Set loading state
        try {
            const response = await api.get('/count-unique-urls-combined');
            setTotalUrls(response.data.message);
            setIsTotalUrlsModalOpen(true);
        } catch (error) {
            console.log(error);
            alert("There was an error fetching the total URLs!", error);
        } finally {
            setIsLoadingTotalUrls(false); // Reset loading state
        }
    };

    const handleCloseTotalUrlsModal = () => {
        setIsTotalUrlsModalOpen(false);
    };

    return (
        <div>
            <div className='flex flex-col gap-9'>
                <div className="flex items-center justify-center shadow-sm shadow-white rounded-md animated-shadow">
                    <p className="text-6xl font-bold text-blue-700 p-2">Welcome To Retrieval Augmented Generation</p>
                </div>
                <div className="font-sans text-xl text-white font-bold flex gap-4 justify-end">
                    <NavLink to="/" className="mx-2 text-xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out hover:border-[#285093] p-2">Home</NavLink>
                    <NavLink to="conversation" className="mx-2 text-xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out hover:border-[#285093] p-2">Conversation</NavLink>
                    <NavLink to="Sources" className="mx-2 text-xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out hover:border-[#285093] p-2">News Sources</NavLink>
                    {/* <h1 className="mx-2 text-xl bg-blue-600 rounded-md p-1 cursor-pointer transition-all duration-300 ease-in-out text-white px-2" onClick={handleTotalUrlsClick}>
                        {isLoadingTotalUrls ? "Loading..." : "Total URLs"}
                    </h1> */}
                    <NavLink to="combined-conversation" className="mx-2 text-xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out hover:border-[#285093] p-2">Combined Conversation</NavLink>
                    <NavLink to="visuals" className="mx-2 text-xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out hover:border-[#285093] p-2">Visuals</NavLink>

                    <h1 className="mx-2 text-xl bg-blue-600 rounded-md p-1 cursor-pointer transition-all duration-300 ease-in-out text-white px-2" onClick={handleTotalCombinedUrlsClick}>
                        {isLoadingTotalUrls ? "Loading..." : "Total URLs"}
                    </h1>
                    <h1 className="mx-2 text-xl bg-red-600 rounded-md p-1 cursor-pointer transition-all duration-300 ease-in-out text-black" onClick={handleDeleteClick}>Delete DB Content</h1>
                </div>
                <Outlet />
                <ConfirmModal
                    isOpen={isModalOpen}
                    onClose={handleCloseModal}
                    onConfirm={handleConfirmDelete}
                />
                <ConfirmURLs
                    isOpen={isTotalUrlsModalOpen}
                    onClose={handleCloseTotalUrlsModal}
                    onConfirm={handleCloseTotalUrlsModal}
                >
                    <p className='text-black text-2xl'>Total unique URLs in the database: {totalUrls}</p>
                </ConfirmURLs>
            </div>
        </div>
    );
};

export default LandingPageLayout;
