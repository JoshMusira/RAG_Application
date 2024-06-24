import React, { useState } from 'react'
import { Outlet } from "react-router-dom";
import { NavLink } from "react-router-dom";
import ConfirmModal from '../components/ConfirmModal ';
import axios from 'axios';

const LandingPageLayout = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
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
            console.log(error)
            alert("There was an error deleting the collection content!", error);
        }
    };

    return (
        <div>
            <div className='flex flex-col gap-9'>

                <div className="flex items-center justify-center shadow-sm shadow-white rounded-md animated-shadow">
                    <p className="text-6xl font-bold text-blue-700 p-2">Welcome To Retrieval Augmented Generation</p>
                </div>
                <div className="  font-sans text-xl text-[#285093] font-bold flex gap-10 justify-end">
                    <NavLink to="/" className="mx-2 text-2xl hover:text-[#3a5da2]  transition-all duration-300 ease-in-out hover:border-[#285093] p-2" >Home</NavLink>
                    <NavLink to="conversation" className="mx-2 text-2xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out  hover:border-[#285093] p-2" >Conversation</NavLink>
                    <h1 className="mx-2 text-2xl bg-red-600 rounded-md p-1 cursor-pointer  transition-all duration-300 ease-in-out text-black  " onClick={handleDeleteClick} >Delete DB Content</h1>
                </div>
                <Outlet />
                <ConfirmModal
                    isOpen={isModalOpen}
                    onClose={handleCloseModal}
                    onConfirm={handleConfirmDelete}
                />

                {/* <QuestionForm /> */}
            </div>
        </div>
    )
}

export default LandingPageLayout