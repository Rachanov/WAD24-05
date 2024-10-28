"use client"

import React, { useState, useEffect } from 'react'
import NavBar from '../components/navbar'
import Link from 'next/link';
import { signIn } from 'next-auth/react'
import { useRouter, redirect } from 'next/navigation'
import { useSession } from 'next-auth/react';
import { FcGoogle } from "react-icons/fc";

function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [rememberMe, setRememberMe] = useState(false);

    const router = useRouter();
    const { data: session } = useSession();

    // Load saved credentials when component mounts
    useEffect(() => {
        const savedCredentials = localStorage.getItem('rememberedCredentials');
        if (savedCredentials) {
            const { email, password } = JSON.parse(savedCredentials);
            setEmail(email);
            setPassword(password);
            setRememberMe(true);
        }
    }, []);

    if (session) router.replace('/');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // Save credentials if remember me is checked
            if (rememberMe) {
                localStorage.setItem('rememberedCredentials', JSON.stringify({ email, password }));
            } else {
                localStorage.removeItem('rememberedCredentials');
            }

            const res = await signIn("credentials", {
                email, password, redirect: false
            })

            if (res.error) {
                setError("Invalid credentials");
                return;
            }

            router.replace("/");

        } catch (error) {
            console.log(error);
        }
    }

    const handleGoogleSignIn = async () => {
        setError(""); // Clear error before Google login
        await signIn("google");
    };

    return (
        <div>
            <NavBar />
            <div className='container mx-auto py-5 flex justify-center items-center min-h-screen'>
                <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white shadow-lg rounded-lg p-6">
                    <h3 className='text-center text-2xl font-semibold'>Login Page</h3>
                    {error && (
                        <div className='bg-red-500 w-fit text-sm text-white py-1 px-3 rounded-md mt-2'>
                            {error}
                        </div>
                    )}

                    <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className='block w-full bg-gray-100 p-2 my-2 rounded-md'
                        type="email"
                        placeholder='your@email.com'
                    />
                    <input
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className='block w-full bg-gray-100 p-2 my-2 rounded-md'
                        type="password"
                        placeholder='Password'
                    />

                    <div className="flex items-center mb-4">
                        <input
                            type="checkbox"
                            id="rememberMe"
                            checked={rememberMe}
                            onChange={(e) => setRememberMe(e.target.checked)}
                            className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <label htmlFor="rememberMe" className="ml-2 text-sm text-gray-700">
                            Remember me
                        </label>
                    </div>

                    <button
                        type='submit'
                        className='bg-black w-full p-2 rounded-md text-white my-2'>
                        Sign In
                    </button>

                    <div className="text-center">
                        <p className='my-2'>or</p>
                        <button type='button' onClick={handleGoogleSignIn} className="bg-white border border-gray-300 rounded-md p-2 flex justify-center items-center w-full mx-auto max-w-sm">

                            <FcGoogle style={{ width: '20px', height: '20px', marginRight: '8px' }} /> Sign up with Google
                        </button>
                        <hr className='my-3' />
                        <p>Don't have an account yet? go to <Link className='text-blue-500 hover:underline' href="/register">Register</Link> Page</p>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default LoginPage