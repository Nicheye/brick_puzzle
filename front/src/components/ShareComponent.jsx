import React, { useState } from 'react';
import axios from 'axios';

const ShareComponent = () => {
  const [isOpen, setIsOpen] = useState(false);

  const handleShare = async (platform) => {
    try {
      const url = 'httlocalhostp://:5173/';
      const message = 'Create Your Image and contribute into Collective Art';
      let shareUrl = '';

      switch (platform) {
        case 'whatsapp':
          shareUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(message)} ${encodeURIComponent(url)}`;
          break;
        case 'telegram':
          shareUrl = `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(message)}`;
          break;
        case 'instagram':
          shareUrl = `https://www.instagram.com/codium_123/`;
          break;
        default:
          console.error('Unsupported platform');
          return;
      }

      window.open(shareUrl, '_blank');

      await axios.get('http://62.113.100.157:8000/api/v1/share', {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true,
      });

      console.log('Share request sent to backend');
    } catch (error) {
      console.error('Error sharing:', error);
    }
  };

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="relative mt-7">
      <div className="flex justify-center ">
        <button
            onClick={toggleModal}
            className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-lg px-5 py-2.5 text-center me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        >
            Share To Get Another Generation
        </button>
        </div>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-semibold mb-4 text-lime-600">Share To get another generation</h2>
            <div className="flex flex-col space-y-2">
              <button
                className="text-white bg-gradient-to-r from-green-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2"
                onClick={() => {
                  handleShare('whatsapp');
                  toggleModal();
                }}
              >
                Share on WhatsApp
              </button>
              <button
                className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2"
                onClick={() => {
                  handleShare('telegram');
                  toggleModal();
                }}
              >
                Share on Telegram
              </button>
              <button
                className="text-white bg-gradient-to-r from-pink-400 via-pink-500 to-pink-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-pink-300 dark:focus:ring-pink-800 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2"
                onClick={() => {
                  handleShare('instagram');
                  toggleModal();
                }}
              >
                Visit Instagram
              </button>
              <button
                className="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
                onClick={toggleModal}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ShareComponent;
