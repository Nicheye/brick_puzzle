import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Developer from './Developer';
import Leaderboard from './LeaderBoard';
const CommonPicture = () => {
    const [common_pic, setCommon_pic] = useState('');
    const [grid, setGrid] = useState('');
    const [images, setImages] = useState([]);
    const [leaders, setLeaders] = useState([]);

    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            window.location.href = '/login';
        } else {
            (async () => {
                try {
                    const { data } = await axios.get('http://62.113.100.157:8000/api/v1/pic', {
                        headers: { 'Content-Type': 'application/json' },
                        withCredentials: true,
                    });
                    setCommon_pic(data.common_pic);
                    setGrid(data.grid);
                    setImages(data.your_images);
                    setLeaders(data.leaderboard);
                    console.log(data.leaderboard)
                } catch (e) {
                    console.log('not auth');
                }
            })();
        }
    }, []);

    return (
        <div className="bg-black p-4 min-h-screen">
            <div className="container mx-auto flex flex-col items-center space-y-8">
                {/* Grid Right Now Section */}
                <div className="w-full max-w-md flex flex-col items-center">
                    <h2 className="text-2xl font-bold text-white mb-4">Grid Right Now</h2>
                    <img
                        src={grid}
                        alt="Grid Right Now"
                        className="w-full h-64 object-cover rounded-lg"
                    />
                </div>

                {/* Common Picture Section */}
                <div className="w-full max-w-md flex flex-col items-center">
                    <h2 className="text-2xl font-bold text-white mb-4">Common Picture</h2>
                    <h4 className="text-lg font-semibold text-gray-300 mb-3">Will be here 17 of August</h4>
                    <img
                        src={common_pic}
                        alt="Common Picture"
                        className="w-full h-64 object-cover rounded-lg"
                    />
                </div>

                {/* Your Images Section */}
                <div className="w-full max-w-md flex flex-col items-center space-y-5">
                    <h3 className="text-lg font-semibold text-gray-300">Your Images</h3>
                    <div className="grid grid-cols-2 gap-4 w-full">
                        {images.map((image, index) => (
                            <img
                                key={index}
                                src={image.image}
                                alt={`Your Image ${index + 1}`}
                                className="w-full h-32 object-cover rounded-lg"
                            />
                        ))}
                    </div>
                </div>
            </div>
            <Leaderboard leaders={leaders}/>
            <Developer/>
        </div>
    );
}

export default CommonPicture;
