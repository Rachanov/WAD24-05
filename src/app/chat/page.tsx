// "use client"
// import React, { useState, useEffect, useRef } from 'react';
// import { Menu } from 'lucide-react';
// import { MessageSquarePlus } from 'lucide-react';
// import { Settings } from 'lucide-react';
// import { CircleHelp } from 'lucide-react';
// import { History } from 'lucide-react';
// import { SendHorizontal } from 'lucide-react';
// import { CircleUserRound } from 'lucide-react';
// import { Smile } from 'lucide-react';
// import { House } from 'lucide-react';
// import { Inbox } from 'lucide-react';
// import Link from 'next/link';


// const ChatComponent: React.FC = () => {
//   const [inputValue, setInputValue] = useState<string>('');
//   const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
//   const [theme, setTheme] = useState<'light' | 'dark'>('light');
//   const textareaRef = useRef<HTMLTextAreaElement>(null);

//   const handleThemeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const newTheme = e.target.checked ? 'dark' : 'light';
//     setTheme(newTheme);
//     document.documentElement.setAttribute('data-theme', newTheme);
//   };

//   const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
//     const textarea = textareaRef.current;
//     if (textarea) {
//       textarea.style.height = "auto"; // รีเซ็ตความสูงก่อนเพื่อคำนวณใหม่
//       textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`; // ปรับความสูงโดยจำกัดที่ maxHeight
//     }
//     setInputValue(e.target.value);
//   };

//   const handleSendMessage = () => {
//     if (inputValue.trim()) {
//       const newMessage = { sender: 'User', text: inputValue };
//       setMessages([...messages, newMessage]);
//       setInputValue('');
//     }
//   };

//   const [isSidebarOpen, setSidebarOpen] = useState(true);

//   const toggleSidebar = () => {
//     setSidebarOpen(!isSidebarOpen);
//   };


//   return (
//     <div className="flex h-screen antialiased text-gray-800 ">
//       {/* content */}
//       <div className="flex flex-row h-full w-full overflow-x-hidden bg-white">
//         {/* left menu section */}
//         <div className={`flex flex-col h-full p-6 py-8 pl-6 pr-2 bg-white text-black transition-all duration-300 ease-in-out ${isSidebarOpen ? 'w-1/6' : 'w-16'
//           }`}>
//           {/* recent(history) */}
//           <div className="flex flex-col mt-0 flex-grow justify-between">
//             <div className="flex flex-row items-center justify-between text-xs">
//               <button onClick={toggleSidebar} className='h-8 w-8'><Menu /></button>
//               {isSidebarOpen && (<label className="swap swap-rotate">
//                 {/* this hidden checkbox controls the state */}
//                 <input type="checkbox" className="theme-controller" value="synthwave" />

//                 {/* sun icon */}
//                 <svg
//                   className="swap-off h-8 w-8 fill-current"
//                   xmlns="http://www.w3.org/2000/svg"
//                   viewBox="0 0 24 24">
//                   <path
//                     d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
//                 </svg>

//                 {/* moon icon */}
//                 <svg
//                   className="swap-on h-8 w-8 fill-current"
//                   xmlns="http://www.w3.org/2000/svg"
//                   viewBox="0 0 24 24">
//                   <path
//                     d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
//                 </svg>
//               </label>)}
//             </div>

//             {/* setting and icon */}
//             {isSidebarOpen && (
//               <div className="flex flex-col mt-0">
//                 {/* <div className="flex flex-row items-center justify-between text-xs mt-0">
//                 <div className='border-t-2 w-full border-[#FFC100]'></div>
//                 </div> */}
//                 <div className="flex flex-col space-y-1 mt-4 ml-3">
//                   <Link href={"/"} className="flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2">
//                     <div><House /></div>
//                     <div className="ml-3 text-xl">Home</div>
//                   </Link>
//                   {/* <button className="flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2">
//                     <div><CircleHelp /></div>
//                     <div className="ml-3 text-xl">Help</div>
//                   </button> */}
//                   <Link href={"/feedback"} className="flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2">
//                     <div><Inbox /></div>
//                     <div className="ml-3 text-xl">Feedback</div>
//                   </Link>
//                   <Link href={"/about-us"} className="flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2">
//                     <div><Smile /></div>
//                     <div className="ml-3 text-xl">About Us</div>
//                   </Link>
//                 </div>
//               </div>
//             )}
//             {isSidebarOpen && (
//               <div className='flex justify-end content-end mb-0'>
//                 <img src="\tree.png" width={1000} height={500} alt="tree-pic" />
//               </div>
//             )}
//           </div>
//         </div>
//         {/* chatsection */}
//         <div className="flex flex-col flex-auto h-full p-6">
//           {/* dronejai */}
//           <div className="flex flex-row items-center h-14 w-full mb-0 justify-between navbar">
//             <Link href={"/"}>
//               <div className="ml-5 text-2xl">Dronejai</div>
//             </Link>
//             <div className="flex-none">

//               <div className="dropdown dropdown-end">
//                 <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
//                   <div className="w-10 rounded-full">
//                     <img
//                       alt="Tailwind CSS Navbar component"
//                       src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
//                   </div>
//                 </div>
//                 <ul
//                   tabIndex={0}
//                   className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
//                   <li>
//                     <a className="justify-between">
//                       Profile
//                     </a>
//                   </li>
//                   <li><a>Settings</a></li>
//                   <li><a>Logout</a></li>
//                 </ul>
//               </div>
//             </div>
//           </div>
//           {/* chatmessage */}
//           <div className="flex flex-col flex-auto flex-shrink-0 rounded-b-2xl h-auto p-4 relative bg-gray-100">
//             {/* <div className='text-[#E6B9A6] border-opacity-8 text-3xl'>Ask me anythings</div> */}

//             {/* Full Height Scrollable Message Section */}
//             <div className="flex flex-col h-full overflow-y-auto w-2/3 mx-auto "> {/* Apply overflow-y-auto to make it scrollable */}
//               <div className="flex flex-col h-full overflow-y-auto">
//                 <div className="grid grid-cols-12 gap-y-2">
//                   {messages.map((message, index) => (
//                     <div key={index} className={`col-start-${message.sender === 'User' ? '6' : '1'} col-end-13 p-3 rounded-lg`}>
//                       <div className={`flex items-center justify-${message.sender === 'User' ? 'start' : 'end'} flex-row-${message.sender === 'User' ? 'reverse' : ''}`}>
//                         <div
//                           className={`relative ${message.sender === 'User' ? 'mr-3' : 'ml-3'} text-sm ${message.sender === 'User' ? 'bg-indigo-100' : 'bg-white'} py-2 px-4 shadow rounded-xl break-words whitespace-pre-wrap`}
//                         >
//                           <div className="text-base break-words">{message.text}</div>
//                         </div>
//                       </div>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             </div>
//             <div className="flex flex-row items-center h-16 rounded-xl bg-white w-2/3 mx-auto px-4">
//               <div className="flex-grow">
//                 <div className="relative w-full">
//                   <textarea
//                     ref={textareaRef}
//                     value={inputValue}
//                     placeholder="Type here"
//                     onChange={handleInputChange}
//                     onKeyPress={(e) => {
//                       if (e.key === 'Enter' && !e.shiftKey) {
//                         e.preventDefault();
//                         handleSendMessage();
//                       }
//                     }}
//                     className="flex w-full border rounded-xl focus:outline-none max-w-full focus:border-indigo-300 pl-4 resize-none overflow-y-auto"
//                     style={{ maxHeight: '200px' }} // จำกัดความสูงสูงสุดของ textarea
//                     rows={1}
//                   />
//                 </div>
//               </div>
//               <div className="ml-4">
//                 <button
//                   className={`flex items-center justify-center text-text-[#2F3645] flex-shrink-0 ${!inputValue ? 'opacity-50 cursor-not-allowed' : ''}`}
//                   disabled={!inputValue}
//                   onClick={handleSendMessage}>
//                   <div><SendHorizontal /></div>
//                 </button>

//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };
// export default ChatComponent;
// import { useTheme } from 'next-themes'
// const { theme, setTheme } = useTheme()
// const handleThemeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//   const newTheme = e.target.checked ? 'dark' : 'light';
//   localStorage.setItem("theme", newTheme)
//   setTheme(newTheme);

//   document.documentElement.setAttribute('data-theme', newTheme);
// };

"use client"
import React, { useState, useEffect, useRef } from 'react';
import { Menu, SendHorizontal, House, Inbox, Smile, User, Bot } from 'lucide-react';
import Link from 'next/link';
import { useTheme } from 'next-themes';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const ChatComponent: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const { theme, setTheme } = useTheme();
  const [mount, setMount] = useState(false);

  useEffect(() => {
    setMount(true);
  }, []);

  if (!mount) {
    return null;
  }

  const handleThemeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTheme = e.target.checked ? 'dark' : 'light';
    localStorage.setItem("theme", newTheme);
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
    setInputValue(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const messageToSend = inputValue.trim();
    setInputValue('');
    setIsLoading(true);

    const newUserMessage: Message = { role: 'user', content: messageToSend };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await axios.post(
        'http://localhost:8000/v1/chat/completions',
        {
          model: "/work_space/LLaMA-Factory/models/llama3_lora_sft",
          messages: [...messages, newUserMessage].map(msg => ({
            role: msg.role,
            content: msg.content
          })),
          temperature: 0.7,
          max_tokens: 1000
        },
        {
          headers: {
            'Authorization': 'Bearer token-abc123',
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.choices && response.data.choices[0]?.message?.content) {
        const botResponse: Message = {
          role: 'assistant',
          content: response.data.choices[0].message.content
        };
        setMessages(prev => [...prev, botResponse]);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'ขออภัย เกิดข้อผิดพลาดในการเชื่อมต่อกับระบบ กรุณาลองใหม่อีกครั้ง'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className={`flex h-screen antialiased ${theme === 'dark' ? 'bg-zinc-700 text-white' : 'bg-white text-gray-800'}`}>
      {/* Sidebar */}
      <div className={`flex flex-col h-full py-8 pl-6 pr-2 ${theme === 'dark' ? 'bg-zinc-800' : 'bg-white'} transition-all duration-300 ease-in-out ${isSidebarOpen ? 'w-64' : 'w-16'}`}>
        <div className="flex flex-col mt-0 flex-grow justify-between">
          <div className="flex flex-row items-center justify-between text-xs">
            <button onClick={toggleSidebar} className="h-8 w-8">
              <Menu className={theme === 'dark' ? 'text-white' : 'text-black'} />
            </button>
            {isSidebarOpen && (
              <label className="swap swap-rotate">
                <input
                  type="checkbox"
                  className="theme-controller"
                  checked={theme === 'dark'}
                  onChange={handleThemeChange}
                />
                {/* Sun icon */}
                {theme === 'light' && (
                  <svg className="swap-off h-8 w-8 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
                  </svg>
                )}
                {/* Moon icon */}
                {theme === 'dark' && (
                  <svg className="swap-on h-8 w-8 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
                  </svg>
                )}
              </label>
            )}
          </div>

          {isSidebarOpen && (
            <div className="flex flex-col mt-8">
              <div className="flex flex-col space-y-1 ml-3">
                <Link href="/" className={`flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2 ${theme === 'dark' ? 'text-white' : 'text-black'}`}>
                  <House />
                  <div className="ml-3 text-xl">Home</div>
                </Link>
                <Link href="/feedback" className={`flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2 ${theme === 'dark' ? 'text-white' : 'text-black'}`}>
                  <Inbox />
                  <div className="ml-3 text-xl">Feedback</div>
                </Link>
                <Link href="/about-us" className={`flex flex-row items-center hover:bg-black hover:text-white rounded-xl p-2 ${theme === 'dark' ? 'text-white' : 'text-black'}`}>
                  <Smile />
                  <div className="ml-3 text-xl">About Us</div>
                </Link>
              </div>
            </div>
          )}

          {isSidebarOpen && (
            <div className="flex justify-end content-end mb-0">
              <img src="/tree.png" width={1000} height={500} alt="tree-pic" />
            </div>
          )}
        </div>
      </div>

      {/* Chat section */}
      <div className={`flex flex-col flex-auto h-full p-6 transition-all duration-300 ease-in-out ${isSidebarOpen ? "ml-0" : "ml-0"} ${theme === 'dark' ? 'bg-zinc-900 text-white' : 'bg-white text-black'}`}>
      <div className={`fixed flex flex-row items-center h-14 ${isSidebarOpen ? 'max-w-[80.5%]' : 'max-w-[91%]'} mb-0 justify-between navbar top-0 z-50 bg-white ${theme === 'dark' ? 'bg-zinc-900 text-white' : 'bg-white'}`}>
            <Link href={"/"}>
              <div className="ml-5 text-2xl">Dronejai</div>
            </Link>
            <div className="flex-none">
              <div className="dropdown dropdown-end z-50">
              </div>
            </div>
          </div>
        {/* Chat messages container */}
        <div className={`flex flex-col flex-auto flex-shrink-0 rounded-2xl h-auto p-4 relative ${theme === 'dark' ? 'bg-zinc-800' : 'bg-gray-100'}`}>
          {/* Messages area */}
          <div className={`flex flex-col h-full w-2/3 mx-auto p-4 ${theme === 'dark' ? 'bg-zinc-800' : 'bg-gray-100'}`}>
            <div className={`flex flex-col h-[calc(100vh-182px)] mt-6 overflow-hidden ${theme === 'dark' ? 'bg-zinc-800' : 'bg-gray-100'}`}>
              <div className="flex flex-col space-y-4 h-full overflow-y-auto" style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex items-start space-x-2 ${
                      message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                    }`}
                  >
                    {/* Icon container */}
                    <div className={`flex-shrink-0 ${message.role === 'user' ? 'ml-2' : 'mr-2'}`}>
                      {message.role === 'user' ? (
                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                          <User className="h-5 w-5 text-blue-600" />
                        </div>
                      ) : (
                        <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                          <Bot className="h-5 w-5 text-gray-600" />
                        </div>
                      )}
                    </div>
                    
                    {/* Message bubble */}
                    <div
                      className={`max-w-[70%] rounded-lg p-3 ${
                        message.role === 'user'
                          ? 'bg-white text-black'
                          : `${theme === 'dark' ? 'bg-zinc-700 text-white' : 'bg-white text-black'}`
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                ))}
                
                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex items-start space-x-2">
                    <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                      <Bot className="h-5 w-5 text-gray-600" />
                    </div>
                    <div className={`rounded-lg p-3 ${theme === 'dark' ? 'bg-zinc-700 text-white' : 'bg-gray-100 text-black'}`}>
                      กำลังพิมพ์...
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Input area */}
          <div className={`flex flex-row items-center h-16 rounded-xl w-2/3 mx-auto px-4 ${theme === 'dark' ? 'bg-zinc-700 border-zinc-600' : 'bg-white border-gray-200'} border`}>
            <div className="flex-grow">
              <div className="relative w-full">
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  placeholder="พิมพ์ข้อความ..."
                  onChange={handleInputChange}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage();
                    }
                  }}
                  className={`flex w-full border rounded-xl focus:outline-none focus:border-blue-300 pl-4 resize-none overflow-y-auto ${
                    theme === 'dark'
                      ? 'bg-zinc-700 text-white border-zinc-600'
                      : 'bg-white text-black border-gray-200'
                  }`}
                  style={{ maxHeight: '200px', scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                  rows={1}
                  disabled={isLoading}
                />
              </div>
            </div>
            <div className="ml-4">
              <button
                className={`flex items-center justify-center flex-shrink-0 hover:text-blue-700
                  ${!inputValue ? 'opacity-50 cursor-not-allowed' : ''}`}
                  disabled={!inputValue}
                  onClick={handleSendMessage}>
                    <SendHorizontal />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  );
};

export default ChatComponent;