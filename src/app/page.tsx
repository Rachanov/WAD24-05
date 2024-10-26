"use client";

import React, { use } from 'react';
import NavBar from './components/navbar';
import "./styles/home.css"
import Link from 'next/link';
import "./homepic.png";

const page: React.FC = () => {
  return (
    <div>
      <NavBar />
      <div className='flex'>
        <div className=' ml-28 mt-36 w-1/2'>
          <p className='text-xl mb-2'>Chat with Dronejai</p>
          <p className='text-5xl font-bold mb-10'>Find out everything about<br />your agriculture drone</p>
          <p className='text-xl mb-5'>Welcome!🌱<br />I'm here to help you explore how agriculture drones work for crop monitoring and field imaging. Let me know if you have any questions or want to learn more!</p>
          <Link href="/chat">
            <button className="px-6 py-2 bg-gradient-to-r from-[#fdf5a8] to-[#ffb0fa] rounded-xl text-xl transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">Start now</button>
          </Link>
        </div>
        <div className='content-end mt-20'>
          <img src="\homepic.png" width={950} height={500} alt="home-pic" />
        </div>
      </div>
    </div>
  );
};

export default page;
