"use client"

import React, { useState, useEffect } from 'react'
import NavBar from '../components/navbar'
import Link from 'next/link';
import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation'

function RegisterPage() {

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    //console.log(name,email,password,confirmPassword)
    const { data: session } = useSession();
    if (session) redirect('/welcome');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password != confirmPassword) {
            setError("Password do not match!");
            return;
        }

        if (!name || !email || !password || !confirmPassword) {
            setError("Please complete all inputs.");
            return;
        }



        try {

            const resCheckUser = await fetch("http://localhost:3000/api/checkUser", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email })
            })

            const { user } = await resCheckUser.json();

            if (user) {
                setError("User already exists.");
                return;
            }
            const res = await fetch("http://localhost:3000/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name, email, password
                })
            })

            if (res.ok) {
                const form = e.target;
                setError("");
                setSuccess("User registration successfully!");
                form.reset();
            } else {
                console.log("User registration failed.")
            }

        } catch (error) {
            console.log("Error during registration: ", error)
        }

    }

    return (
        <div>
            <NavBar />
            <div className='container mx-auto py-5'>
                <h3>Register Page</h3>
                <hr className='my-3' />
                <form onSubmit={handleSubmit}>

                    {error && (
                        <div className='bg-red-500 w-fit text-sm text-white py-1 px-3 rounded-md mt-2'>
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className='bg-green-500 w-fit text-sm text-white py-1 px-3 rounded-md mt-2'>
                            {success}
                        </div>
                    )}

                    <input onChange={(e) => setName(e.target.value)} className='block bg-gray-300 p-2 my-2 rounded-md' type="text" placeholder='Enter you name' />
                    <input onChange={(e) => setEmail(e.target.value)} className='block bg-gray-300 p-2 my-2 rounded-md' type="email" placeholder='Enter you email' />
                    <input onChange={(e) => setPassword(e.target.value)} className='block bg-gray-300 p-2 my-2 rounded-md' type="password" placeholder='Enter you password' />
                    <input onChange={(e) => setConfirmPassword(e.target.value)} className='block bg-gray-300 p-2 my-2 rounded-md' type="password" placeholder='Confirm your password' />
                    <button type='submit' className='bg-green-500 p-2 rounded-md text-white'>Sign Up</button>
                </form>
                <hr className='my-3' />
                <p>Already have an account? go to <Link className='text-blue-500 hover:underline' href="/login">Login</Link> Page</p>
            </div>
        </div>
    )
}

export default RegisterPage
