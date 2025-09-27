import { useState } from "react";

export default function PortfolioManagement() {
  //const [balance, setBalance] = useState(1000);

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Left Sidebar - Portfolio */}
      <aside className="w-1/4 bg-white shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">📊 Portfolio</h2>
        <p className="mb-4 text-gray-700">


        </p>
        <ul className="space-y-2">
          <li className="flex justify-between border-b pb-1 text-gray-700">
            <span>YouTube Music</span>
            <span>$250</span>
          </li>
          <li className="flex justify-between border-b pb-1 text-gray-700">
            <span>TikTok Trends</span>
            <span>$150</span>
          </li>
        </ul>
      </aside>

      <main className="flex-1 p-8">
        <h1 className="text-2xl font-bold mb-6">Market Dashboard</h1>
        <div className="bg-white rounded-xl shadow-md p-6 h-96 flex items-center justify-center">
          /* Placeholder for Chart.js */
          <p className="text-gray-400"> </p>
        </div>
      </main>


      <aside className="w-1/4 bg-white shadow-md p-6 flex flex-col">
        <h2 className="text-xl font-bold mb-4">🤖 Chatbot</h2>
        <div className="flex-1 bg-gray-50 p-3 rounded-md text-gray-600 overflow-y-auto">
          <p>AI Assistant is here to help</p>
        </div>
        <input
          type="text"
          placeholder="Ask anything..."
          className="mt-4 p-2 border rounded-md"
        />
      </aside>



    </div>
  );
}