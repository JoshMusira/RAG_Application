// ConfirmModal.js
import React from 'react';

const ConfirmModal = ({ isOpen, onClose, onConfirm }) => {

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0  flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-gray-600 p-6 rounded shadow-lg">
                <h2 className="text-xl mb-4">Confirm Deletion</h2>
                <p>Are you sure you want to delete the database content?</p>
                <div className="mt-4 flex justify-end gap-4">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-black rounded hover:bg-gray-400"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={onConfirm}
                        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                    >
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmModal;
