import React, { useState } from 'react'

const Expander = ({ title, content, source }) => {
    const [isOpen, setIsOpen] = useState(false);
    return (
        <div className="expander">
            <b onClick={() => setIsOpen(!isOpen)} className="expander-title">{title}</b>
            {isOpen && <p className="expander-content">{content}</p>}
            {isOpen && <p className="text-red-600 cursor-pointer"><span className='fond-bold text-blue-700 text-2xl pr-2'>Source:</span>{source}</p>}
        </div>
    );
}

export default Expander