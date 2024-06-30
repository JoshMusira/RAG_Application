import React from 'react'

const ConfirmURLs = ({ isOpen, onClose, onConfirm, children }) => {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-5 rounded shadow-lg">
                {children}
                <div className="flex justify-end gap-2 mt-4">
                    <button onClick={onClose} className="bg-gray-300 px-4 py-2 rounded">Cancel</button>
                    <button onClick={onConfirm} className="bg-blue-500 text-white px-4 py-2 rounded">OK</button>
                </div>
            </div>
        </div>
    )
}

export default ConfirmURLs

