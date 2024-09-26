"use client"
import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { MessageSquarePlus } from 'lucide-react';
import { Settings } from 'lucide-react';
import { CircleHelp } from 'lucide-react';
import { History } from 'lucide-react';
import { SendHorizontal } from 'lucide-react';
import { CircleUserRound } from 'lucide-react';
import Link from 'next/link';


const ChatComponent: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>('');
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      const newMessage = { sender: 'User', text: inputValue };
      setMessages([...messages, newMessage]);
      setInputValue('');
    }
  };

  return (
    <div className="flex h-screen antialiased text-gray-800 ">
      {/* content */}
      <div className="flex flex-row h-full w-full overflow-x-hidden  bg-[#2F3645]" >
        {/* left menu section */}
        <div className="flex flex-col space h-full p-6 py-8 pl-6 pr-2 w-64 flex-shrink-0 bg-[#2F3645] text-white">
          {/* recent(history) */}
          <div className="flex flex-col mt-0 flex-grow">
            <div className="flex flex-row items-center justify-between text-xs">
              <button><Menu /></button>
              <button><MessageSquarePlus /></button>
            </div>
            <div className="flex flex-row items-center text-xs">
              <span className="text-3xl text-[#E6B9A6] mt-5">Recent</span>
            </div>

            {/* <div className="flex flex-col space-y-1 mt-4 -mx-2 h-48 overflow-y-auto">
              {/* Conversation list
              <button className="flex flex-row items-center hover:bg-gray-100 rounded-xl p-2">
                <div className="ml-2 text-sm font-semibold">Henry Boyd</div>
              </button>
              <button className="flex flex-row items-center hover:bg-gray-100 rounded-xl p-2">
                <div className="ml-2 text-sm font-semibold">Marta Curtis</div>
              </button>
              <button className="flex flex-row items-center hover:bg-gray-100 rounded-xl p-2">
                <div className="ml-2 text-sm font-semibold">Philip Tucker</div>
              </button>
            </div> 
            {/* setting and icon */}
            <div className="flex flex-col mt-auto">
              <div className="flex flex-row items-center justify-between text-xs mt-6">
                <div className='border-t-2 w-full border-[#E6B9A6]'></div>
              </div>
              <div className="flex flex-col space-y-1 mt-4 -mx-2">
                <button className="flex flex-row items-center hover:bg-[#E6B9A6] hover:text-[#2F3645] rounded-xl p-2">
                  <div><History /></div>
                  <div className="ml-2 text-xl font-semibold">History</div>
                </button>
                <button className="flex flex-row items-center hover:bg-[#E6B9A6] hover:text-[#2F3645] rounded-xl p-2">
                  <div><CircleHelp /></div>
                  <div className="ml-2 text-xl font-semibold">Help</div>
                </button>
                <button className="flex flex-row items-center hover:bg-[#E6B9A6] hover:text-[#2F3645] rounded-xl p-2">
                  <div><Settings /></div>
                  <div className="ml-2 text-xl font-semibold">Setting</div>
                </button>
              </div>
            </div>
          </div>
        </div>
        {/* chatsection */}
        <div className="flex flex-col flex-auto h-full p-6">
          {/* dronejai */}
          <div className="flex flex-row items-center h-12 w-full mb-0 bg-white rounded-t-2xl border-b-2 border-[#E6B9A6]">
            {/* <div className="flex items-center justify-center rounded-2xl text-indigo-700 bg-indigo-100 h-10 w-10">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div> */}
            <Link href={"/"}>
            <div className="ml-3 font-bold text-2xl">Dronejai</div>
            </Link>
          </div>
          {/* chatmessage */}
          <div className="flex flex-col flex-auto flex-shrink-0 rounded-b-2xl bg-gray-100 h-auto p-4 ">
            {/* <div className='text-[#E6B9A6] border-opacity-8 text-3xl'>Ask me anythings</div> */}
            <div className="flex flex-col h-full overflow-x-auto mb-4">
              <div className="flex flex-col h-full">
                <div className="grid grid-cols-12 gap-y-2">
                  {messages.map((message, index) => (
                    <div key={index} className={`col-start-${message.sender === 'User' ? '6' : '1'} col-end-13 p-3 rounded-lg`}>
                      <div className={`flex items-center justify-${message.sender === 'User' ? 'start' : 'end'} flex-row-${message.sender === 'User' ? 'reverse' : ''}`}>
                        {/* profile user */}
                        <div className="flex items-center justify-center w-10 rounded-full flex-shrink-0"><CircleUserRound size={30} /></div>
                        <div className={`relative ${message.sender === 'User' ? 'mr-3' : 'ml-3'} text-sm ${message.sender === 'User' ? 'bg-indigo-100' : 'bg-white'} py-2 px-4 shadow rounded-xl`}>
                          <div className='text-xl'>{message.text}</div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* <div className="col-start-1 col-end-8 p-3 rounded-lg">
                    <div className="flex flex-row items-center">
                      <div className="flex items-center justify-center h-10 w-10 rounded-full bg-indigo-500 flex-shrink-0">A</div>
                      <div className="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl">
                        <div>Hey, how are you today?</div>
                      </div>
                    </div>
                  </div>

                  <div className="col-start-6 col-end-13 p-3 rounded-lg">
                    <div className="flex items-center justify-start flex-row-reverse">
                      <div className="flex items-center justify-center h-10 w-10 rounded-full bg-indigo-500 flex-shrink-0">A</div>
                      <div className="relative mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl">
                        <div>I'm ok, what about you?</div>
                      </div>
                    </div>
                  </div> */}


                </div>
              </div>
            </div>
            {/* input */}
            <div className="flex flex-row items-center h-16 rounded-xl bg-white w-full px-4">
              {/* <div>
                <button className="flex items-center justify-center text-gray-400 hover:text-gray-600">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                    />
                  </svg>
                </button>
              </div> */}
              <div className="flex-grow">
                <div className="relative w-full">
                  <input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    onKeyPress={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
                    className="flex w-full border rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10"
                  />
                </div>
              </div>
              <div className="ml-4">
                <button
                  className={`flex items-center justify-center text-text-[#2F3645] flex-shrink-0 ${!inputValue ? 'opacity-50 cursor-not-allowed' : ''}`}
                  disabled={!inputValue}
                  onClick={handleSendMessage}>
                  <div><SendHorizontal /></div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;