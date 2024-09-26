"use client";

import React, { use } from 'react';
import Navbar from '../components/navbar';
import { useSession } from "next-auth/react";
import "../styles/home.css"
import Link from 'next/link';
import { redirect } from "next/navigation";
function WelcomePage() {

    const { data: session } = useSession();
    if (!session) redirect("/login");
    console.log(session)

    return (
        <div>
            <Navbar session={session}/>
            <div className='content'>
                <p className='text-xl'>Welcome, {session?.user?.name} </p>
                <p className='text-xl'>Your email address: {session?.user?.email}</p>
                <p className='text-xl'>Chat with Dronejai</p>
                <p className='text-3xl m-1'>Find out everything about your</p>
                <p className='text-5xl mb-4'>Agriculture drone</p>
                <Link href="/chat">
                    <button className="startButton ">Start now</button>
                </Link>
            </div>
        </div>
    );
};

export default WelcomePage;
