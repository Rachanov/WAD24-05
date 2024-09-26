

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
import "./styles/home.css"
import { useSession } from "next-auth/react";


export default function Home() {

  const { data: session } = useSession();

  return (
    <main>
      <Navbar session={session}/>
      <div className='content'>
        <p className='text-xl'>Chat with Dronejai</p>
        <p className='text-3xl m-1'>Find out everything about your</p>
        <p className='text-5xl mb-4'>Agriculture drone</p>
        <Link href="/chat">
          <button className="startButton ">Start now</button>
        </Link>
      </div>
    </main>
  );
}