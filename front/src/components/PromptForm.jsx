import React, { useState } from 'react';
import axios from 'axios';
import anime_icon from '../assets/icons/anime.png';
import cnm_icon from '../assets/icons/cnm.png';
import goth_icon from '../assets/icons/goth.png';
import minim_icon from '../assets/icons/minim.png';
import sci_icon from '../assets/icons/sci.png';

const PromptForm = () => {
  const [prompt, setPrompt] = useState('');
  const [style, setStyle] = useState('');
  const [color, setColor] = useState('');
  const [openDropdown, setOpenDropdown] = useState(null); // Track which dropdown is open

  const styles = [
    { value: 'AN', label: 'Anime', icon: anime_icon },
    { value: 'GOTH', label: 'Gothic', icon: goth_icon },
    { value: 'Sci-Fi', label: 'Sci-Fi', icon: sci_icon },
    { value: 'CNM', label: 'Cinematic', icon: cnm_icon },
    { value: 'MN', label: 'Minimalistic', icon: minim_icon }
  ];

  const colors = [
    { value: 'BW', label: 'Black and white', colorCode: ['#000000', '#999'] }, // Two colors for BW
    { value: 'Yel', label: 'Yellow', colorCode: ['#FFFF00'] },
    { value: 'br', label: 'Bright', colorCode: ['#FF5733'] },
    { value: 'dr', label: 'Dark and gloomy', colorCode: ['#4A4A4A'] },
    { value: 'pl', label: 'Pastel colors', colorCode: ['#FFB6C1'] }
  ];

  const handleStyleChange = (value) => {
    setStyle(value);
    setOpenDropdown(null); // Close dropdown after selection
  };

  const handleColorChange = (value) => {
    setColor(value);
    setOpenDropdown(null); // Close dropdown after selection
  };

  const toggleDropdown = (dropdown) => {
    setOpenDropdown(openDropdown === dropdown ? null : dropdown);
  };

  const submit = async e => {
    e.preventDefault();

    const payload = {
      prompt: prompt,
      style: style,
      color: color
    };
    
    const config = {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    };

    try {
      const { data } = await axios.post('http://62.113.100.157:8000/api/v1/', payload, config);
      console.log('Response:', data); // Log response for debugging
    } catch (error) {
      console.error('Request failed:', error.response ? error.response.data : error.message);
    }
  };

  return (
    <div className="flex flex-col items-center p-6">
      <form className='w-full max-w-lg bg-white border border-gray-300 rounded-lg shadow-lg p-6 space-y-6' onSubmit={submit}>
        <div className="mb-6">
          <label htmlFor="prompt" className="block text-gray-700 text-lg font-medium mb-2">Enter your idea and style here ✔</label>
          <input
            id="prompt"
            value={prompt}
            required
            onChange={e => setPrompt(e.target.value)}
            placeholder='Enter your idea here'
            type="text"
            className="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-300 text-base focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        {/* Style Dropdown */}
        <div className="relative mb-4">
          <button
            type="button"
            onClick={() => toggleDropdown('style')}
            className="w-full bg-gray-300 text-gray-700 text-sm rounded-lg flex justify-between items-center p-3 hover:bg-gray-200 focus:ring-blue-500 focus:border-blue-500"
          >
            <span>{style || 'Select style'}</span>
            <svg className="w-4 h-4 ml-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {openDropdown === 'style' && (
            <div className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg">
              {styles.map((styleOption) => (
                <div
                  key={styleOption.value}
                  onClick={() => handleStyleChange(styleOption.value)}
                  className="flex items-center p-3 cursor-pointer hover:bg-gray-100"
                >
                  <img src={styleOption.icon} alt={styleOption.label} className="w-6 h-6 mr-3" />
                  <span className="text-gray-700">{styleOption.label}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Color Dropdown */}
        <div className="relative">
          <button
            type="button"
            onClick={() => toggleDropdown('color')}
            className="w-full bg-gray-300 text-gray-700 text-sm rounded-lg flex justify-between items-center p-3 hover:bg-gray-200 focus:ring-blue-500 focus:border-blue-500"
          >
            <span>{color || 'Select color'}</span>
            <svg className="w-4 h-4 ml-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {openDropdown === 'color' && (
            <div className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg">
              {colors.map((colorOption) => (
                <div
                  key={colorOption.value}
                  onClick={() => handleColorChange(colorOption.value)}
                  className="flex items-center p-3 cursor-pointer hover:bg-gray-100"
                >
                  {colorOption.colorCode.map((color, index) => (
                    <div
                      key={index}
                      style={{ backgroundColor: color }}
                      className="w-4 h-4 rounded-full border border-gray-400 mr-2"
                    />
                  ))}
                  <span className="text-gray-700">{colorOption.label}</span>
                </div>
              ))}
            </div>
          )}
        </div>
        <button 
          type="submit" 
          className="w-full text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center"
        >
          Generate ✨
        </button>
      </form>
    </div>
  );
};

export default PromptForm;
