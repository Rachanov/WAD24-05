import React from 'react';
import '../styles/navbarStyle.css';

const NavBar: React.FC = () => {
  return (
    <nav className="flex justify-between bg-[#2F3645] text-white">
      <div className="flex">
        <a href="#home" className="p-4 hover:bg-[#E6B9A6]">Dronejai</a>
        <a href="#about-us" className='p-4 hover:bg-[#E6B9A6]'>About Us</a>
        <a href="#feedback" className='p-4 hover:bg-[#E6B9A6]'>Feedback</a>
      </div>
      <div className="content-center px-3">
        <button className="text-black bg-[#FFD369] rounded-md p-1.5 px-2.5 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">Log In</button>
        <button className="text-black bg-white rounded-md p-1.5 px-2.5 ml-3 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">Sign Up</button>
      </div>
    </nav>

  );
};

export default NavBar;