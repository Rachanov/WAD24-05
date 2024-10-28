"use client";

import React, { useState, useEffect, useRef } from 'react';
import Link from "next/link";
import { signOut, useSession } from 'next-auth/react';

function Navbar() {
    const { data: session } = useSession(); // Get session directly in Navbar
    const colors = ["bg-red-500", "bg-blue-500", "bg-green-500", "bg-yellow-500", "bg-purple-500", "bg-pink-500"];
    const [profileColor, setProfileColor] = useState(colors[0]);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const getColor = () => {
            const storedColor = window.localStorage.getItem("profileColor");
            if (storedColor) {
                return storedColor;
            }
            const newColor = colors[Math.floor(Math.random() * colors.length)];
            window.localStorage.setItem("profileColor", newColor);
            return newColor;
        };

        setProfileColor(getColor());
    }, [colors]);

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    const handleSignOut = () => {
        window.localStorage.removeItem("profileColor");
        signOut();
    };

    const buttonDic = [
        { text: "Home", href: "/" },
        { text: "Feedback", href: "/feedback" },
        { text: "About Us", href: "/about-us" }
    ];

    return (
        <nav className="flex justify-between items-center bg-white text-black h-16 px-4 pt-4">
            <div className="flex items-center ml-14 flex-1">
                <Link href="/" className="text-2xl">
                    Dronejai
                </Link>
            </div>

            <div className="flex items-center justify-center flex-1">
                {buttonDic.map((buttonData, index) => (
                    <Link
                        href={buttonData.href}
                        key={index}
                        className='p-4 after:duration-500 ease-out after:block after:h-0.5 after:w-full after:origin-bottom-center after:scale-x-0 after:bg-black after:transition-transform after:hover:origin-bottom-center after:hover:scale-x-100'
                    >
                        {buttonData.text}
                    </Link>
                ))}
            </div>

            <div className="flex items-center justify-end flex-1 mr-14">
                {!session ? (
                    <>
                        <Link href="/register">
                            <button className="text-white bg-black border-black border-2 rounded-xl w-28 py-1.5 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
                                Sign Up
                            </button>
                        </Link>
                        <Link href="/login">
                            <button className="bg-white rounded-xl border-black border-2 w-28 py-1.5 ml-3 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
                                Log In
                            </button>
                        </Link>
                    </>
                ) : (
                    <div className="flex items-center space-x-3">
                        <div
                            onClick={toggleDropdown}
                            className={`cursor-pointer w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${profileColor}`}
                        >
                            {session.user.name?.[0].toUpperCase()}
                        </div>

                        {dropdownOpen && (
                            <div ref={dropdownRef} className="absolute top-12 right-0 mt-2 w-48 bg-white rounded-md shadow-lg overflow-hidden z-10">
                                <Link href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100">
                                    My Account
                                </Link>
                                <Link href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100">
                                    Settings
                                </Link>
                                <hr className="border-t border-gray-200 my-1" />
                                <button
                                    onClick={handleSignOut}
                                    className="block w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100"
                                >
                                    Log out
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
