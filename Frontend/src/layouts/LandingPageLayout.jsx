import React from 'react'
import { Outlet } from "react-router-dom";
import { NavLink } from "react-router-dom";

const LandingPageLayout = () => {
    return (
        <div>
            <div className='flex flex-col gap-9'>

                <div className="flex items-center justify-center shadow-sm shadow-white rounded-md animated-shadow">
                    <p className="text-6xl font-bold text-blue-700 p-2">Welcome To Retrieval Augmented Generation</p>
                </div>
                <div className="  font-sans text-xl text-[#285093] font-bold flex justify-end">
                    <NavLink to="/" className="mx-2 text-3xl hover:text-[#3a5da2] border-b-2 transition-all duration-300 ease-in-out hover:border-[#285093] " >Home</NavLink>
                    <NavLink to="conversation" className="mx-2 text-3xl hover:text-[#3a5da2] transition-all duration-300 ease-in-out hover:border-[#285093] " >Conversation</NavLink>
                </div>
                <Outlet />

                {/* <QuestionForm /> */}
            </div>
        </div>
    )
}

export default LandingPageLayout