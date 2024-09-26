import React from 'react';
import '../styles/navbarStyle.css';

const NavBar: React.FC = () => {
  return (
    <nav className="flex justify-between bg-[#2F3645] text-white text-xl">
      <div className="flex">
        <a href="#home" className="p-4 hover:bg-[#E6B9A6] hover:text-[#2F3645]">Dronejai</a>
        <a href="#about-us" className='p-4 hover:bg-[#E6B9A6] hover:text-[#2F3645]'>About Us</a>
        <a href="#feedback" className='p-4 hover:bg-[#E6B9A6] hover:text-[#2F3645]'>Feedback</a>
      </div>
      <div className="content-center px-3">
        <button className="text-black bg-[#E1D7B7] rounded-2xl p-1.5 px-2.5 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">Log In</button>
        <button className="text-black bg-white rounded-2xl p-1.5 px-2.5 ml-3 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">Sign Up</button>
      </div>
    </nav>

  );
};

export default NavBar;