"use client";

import { useState } from "react";
import NavBar from '../components/navbar'

export default function ContactForm() {
  const [fullname, setFullname] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState([]);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("Full name: ", fullname);
    console.log("Email: ", email);
    console.log("Message: ", message);

    const res = await fetch("api/contact", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        fullname,
        email,
        message,
      }),
    });

    const { msg, success } = await res.json();
    setError(msg);
    setSuccess(success);

    if (success) {
      setFullname("");
      setEmail("");
      setMessage("");
    }
  };

  return (
    <>
      <NavBar />
      <div className="max-w-2xl mx-auto mt-8 px-4">
        <h1 className="text-3xl font-bold text-center mb-2">Contact Us</h1>
        <p className="text-center mb-8">Please fill in the form below</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex flex-col">
            <label htmlFor="fullname" className="mb-2 text-sm">Full Name</label>
            <input
              onChange={(e) => setFullname(e.target.value)}
              value={fullname}
              type="text"
              id="fullname"
              placeholder="john"
              className="p-3 rounded bg-gray-50 border border-gray-200"
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="email" className="mb-2 text-sm">Email</label>
            <input
              onChange={(e) => setEmail(e.target.value)}
              value={email}
              type="email"
              id="email"
              placeholder="john@gmail.com"
              className="p-3 rounded bg-gray-50 border border-gray-200"
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="message" className="mb-2 text-sm">Your Message</label>
            <textarea
              onChange={(e) => setMessage(e.target.value)}
              value={message}
              id="message"
              placeholder="Hi Hello"
              className="p-3 rounded bg-gray-50 border border-gray-200 h-32 resize-none"
            ></textarea>
          </div>

          <button 
            className="w-full bg-green-700 hover:bg-green-800 text-white font-semibold p-3 rounded transition-colors" 
            type="submit"
          >
            Send
          </button>
        </form>

        <div className="mt-4">
          {error &&
            error.map((e, index) => (
              <div
                key={index}
                className={`${
                  success ? "text-green-800 bg-gray-50" : "text-red-600 bg-gray-50"
                } px-5 py-2`}
              >
                {e}
              </div>
            ))}
        </div>
      </div>
    </>
  );
}