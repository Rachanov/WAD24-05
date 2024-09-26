"use client"
import React from 'react';
import Link from "next/link";
import '../styles/navbarStyle.css';
import { signOut } from 'next-auth/react'

function Navbar({ session }) {
  return (
    <nav className="flex justify-between bg-[#2F3645] text-white">
      <div className="flex">
        <a href="/" className="p-4 hover:bg-[#E6B9A6]">Dronejai</a>
        <a href="#about-us" className='p-4 hover:bg-[#E6B9A6]'>About Us</a>
        <a href="#feedback" className='p-4 hover:bg-[#E6B9A6]'>Feedback</a>
      </div>
      <div className="content-center px-3">
        {!session ? (
          <>
            <button className="text-black bg-[#FFD369] rounded-md p-1.5 px-2.5 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300" ><Link href="/login">Log In</Link></button>
            <button className="text-black bg-white rounded-md p-1.5 px-2.5 ml-3 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300"><Link href="/register">Sign Up</Link></button>
          </>
        ) : ( 
          <button className="text-black bg-red-500 rounded-md p-1.5 px-2.5 ml-3 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300"><a onClick={() => signOut()}>Logout</a></button>
        )}


      </div>
    </nav>

  )
}

export default Navbar;