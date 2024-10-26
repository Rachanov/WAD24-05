"use client";

import React, { use } from 'react';
import NavBar from '../components/navbar';
import "../styles/home.css"
import Link from 'next/link';

const aboutpage: React.FC = () => {
    const images = [
        { src: "../team2.png", text: "Korapatr Lertwithayakul" },
        { src: "../team1.png", text: "Nititorn Prompila" },
        { src: "../team3.png", text: "Ganpapath Pheephokinanan" }
    ];

    return (
        <div>
            <NavBar />
            <div className='flex justify-center items-center'>
                <div className='flex justify-center w-1/3'>
                    <img src="..\team.png" width={800} height={500} alt="team-pic" />
                </div>
                <div className='w-1/2'>
                    <p className="flex justify-center content-center text-center text-2xl font-bold">Meet our team!</p>
                    <div className="flex justify-center gap-4 p-4">
                        {images.map((image, index) => (
                            <div key={index} className="border rounded-lg shadow-md p-4 w-60 flex flex-col items-center">
                                <img
                                    src={image.src}
                                    alt={image.text}
                                    className="rounded-md mb-2"
                                />
                                <p className="text-center">{image.text}</p>
                            </div>
                        ))}
                    </div>
                    <p className="flex justify-center content-center text-center text-lg">We are students from Khon Kaen University.<br />This web application was developed based on our instructor’s recommendation, as we saw it as an excellent opportunity to enhance our skills in various fields.
                        Additionally, we aim to facilitate easy, efficient access to information and knowledge about agricultural drones for those interested.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default aboutpage;
