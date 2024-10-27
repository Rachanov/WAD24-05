import React from 'react';
import '../styles/navbarStyle.css';
import Link from 'next/link';


const NavBar: React.FC = () => {

  const buttonDic = [{ text: "Home", href: "/" }, { text: "Feedback", href: "/feedback" }, { text: "About Us", href: "/about-us" }]


  return (
    <nav className=" bg-white pt-4 text-black text-xl flex">
      <table className='w-full table-fixed'>
        <thead>
          <tr className='flex justify-between'>
            <td className='flex items-start justify-start ml-14 flex-1'><Link href="/" className="py-4 text-black text-2xl">Dronejai</Link></td>
            <td className="flex items-center justify-center flex-1">
              {buttonDic.map((buttonData, index) => (
                <Link href={buttonData.href} key={index} className='p-4 after:duration-500 ease-out after:block after:h-0.5 after:w-full after:origin-bottom-center after:scale-x-0 after:bg-black after:transition-transform after:hover:origin-bottom-center after:hover:scale-x-100'>{buttonData.text}</Link>
              ))}
            </td>
            <td className="flex items-center justify-end flex-1 mr-14">
                <button className="btn btn-neutral text-white bg-black border-black border-2 rounded-xl w-28 py-1.5">Sign Up</button>
                <button className="btn bg-white rounded-xl border-black border-2 w-28 py-1.5 ml-3">Log In</button>
            </td>
          </tr>
        </thead>
      </table>
    </nav>
  );
};

export default NavBar;