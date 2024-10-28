

// import React, { use } from 'react';
// import NavBar from './components/navbar';
// import "./styles/home.css"
// import Link from 'next/link';
// const page: React.FC = () => {
//   return (
//     <div>
//       <NavBar /> 
//       <div className='content'>
//         <p className='text-xl'>Chat with Dronejai</p>
//         <p className='text-3xl m-1'>Find out everything about your</p>
//         <p className='text-5xl mb-4'>Agriculture drone</p>
//         <Link href="/chat">
//         <button className="startButton ">Start now</button>
//         </Link>
//       </div>
//     </div>
//   );
// };

// export default page;

"use client";

import Navbar from "./components/navbar";
import Link from 'next/link';
import "./styles/home.css";
import { useSession } from "next-auth/react";
import { useRouter } from 'next/navigation';

export default function Home() {
  const { data: session, status } = useSession();
  const router = useRouter();

  // If there is no session and the status is "unauthenticated", redirect to login
  // if (status === "unauthenticated") {
  //   router.push("/login");
  //   return null; // Prevents further rendering
  // }

  return (
    <main>
      <Navbar session={session} />
      <div className='flex'>
        <div className='ml-28 mt-36 w-1/2'>
          {session ? (
            <>
              <p className='text-xl mb-2'>Chat with Dronejai</p>
              <p className='text-5xl font-bold mb-10'>Find out everything about<br />your agriculture drone</p>
              <p className='text-xl mb-2'>Welcome, {session.user?.name} 🌱</p>
              <p className='text-xl mb-2'>Your email address: {session.user?.email}</p>
              {/* <p className='text-xl mb-5'>I'm here to help you explore how agriculture drones work for crop monitoring and field imaging. Let me know if you have any questions or want to learn more!</p> */}
            </>
          ) : (
            <>
              <p className='text-xl mb-2'>Chat with Dronejai</p>
              <p className='text-5xl font-bold mb-10'>Find out everything about<br />your agriculture drone</p>
              <p className='text-xl mb-5'>Welcome!🌱<br />I'm here to help you explore how agriculture drones work for crop monitoring and field imaging. Let me know if you have any questions or want to learn more!</p>
            </>
          )}
          <Link href="/chat">
            <button className="px-6 py-2 bg-gradient-to-r from-[#fdf5a8] to-[#ffb0fa] rounded-xl text-xl transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
              Start now
            </button>
          </Link>
        </div>
        <div className='content-end mt-20'>
          <img src="\homepic.png" width={950} height={500} alt="home-pic" />
        </div>
      </div>
    </main>
  );
}
