// "use client";

// import React, { use } from 'react';
// import Navbar from '../components/navbar';
// import { useSession } from "next-auth/react";
// import "../styles/home.css"
// import Link from 'next/link';
// import { redirect } from "next/navigation";
// function WelcomePage() {

//     const { data: session } = useSession();
//     if (!session) redirect("/login");
//     console.log(session)

//     return (
//         <main>
//             <Navbar session={session} />
//             <div className='flex'>
//                 <div className=' ml-28 mt-36 w-1/2'>
//                     {/* <p className='text-xl mb-2'>Welcome, {session?.user?.name} </p>
//                     <p className='text-xl mb-2'>Your email address: {session?.user?.email}</p> */}
//                     <p className='text-xl mb-2'>Chat with Dronejai</p>
//                     <p className='text-5xl font-bold mb-10'>Find out everything about<br />your agriculture drone</p>
//                     <p className='text-xl mb-5'>Welcome! {session?.user?.name} 🌱<br />Your email address: {session?.user?.email}</p>
//                     <Link href="/chat">
//                         <button className="px-6 py-2 bg-gradient-to-r from-[#fdf5a8] to-[#ffb0fa] rounded-xl text-xl transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">Start now</button>
//                     </Link>
//                 </div>
//                 <div className='content-end mt-20'>
//                     <img src="\homepic.png" width={950} height={500} alt="home-pic" />
//                 </div>
//             </div>
//         </main>
//         // <div>
//         //     <Navbar session={session}/>
//         //     <div className='content'>
//         //         <p className='text-xl'>Welcome, {session?.user?.name} </p>
//         //         <p className='text-xl'>Your email address: {session?.user?.email}</p>
//         //         <p className='text-xl'>Chat with Dronejai</p>
//         //         <p className='text-3xl m-1'>Find out everything about your</p>
//         //         <p className='text-5xl mb-4'>Agriculture drone</p>
//         //         <Link href="/chat">
//         //             <button className="startButton ">Start now</button>
//         //         </Link>
//         //     </div>
//         // </div>
//     );
// };

// export default WelcomePage;
