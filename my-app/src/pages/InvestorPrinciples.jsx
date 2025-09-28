import { useState, useEffect } from "react";

export default function InvestorPrinciples() {
  const [balance, setBalance] = useState(1000);
  const [geminiData, setGeminiData] = useState(null); // API response
  const [loading, setLoading] = useState(true);

  // Fetch Gemini API data from backend
  useEffect(() => {
    async function fetchGeminiData() {
      try {
        const response = await fetch("http://localhost:5000/analyze/"); // your Flask route
        const data = await response.json ? await response.json() : { text: await response.text() };
        setGeminiData(data);
      } catch (error) {
        console.error("Error fetching Gemini data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchGeminiData();
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Left Sidebar - Portfolio */}
      <aside className="w-1/4 bg-white shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">📊 Portfolio</h2>
        <p className="mb-4 text-gray-700">
          Balance: <span className="font-semibold">${balance}</span>
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

      {/* Middle - Market Data / Chart */}
      <main className="flex-1 p-8">
        <h1 className="text-2xl font-bold mb-6">Market Dashboard</h1>
        <div className="bg-white rounded-xl shadow-md p-6 h-96 flex items-center justify-center overflow-y-auto">
          {loading ? (
            <p className="text-gray-400">Loading AI analysis...</p>
          ) : (
            <p className="text-gray-800 whitespace-pre-wrap">{geminiData?.text || "No data available"}</p>
          )}
        </div>
      </main>

      {/* Right Sidebar - Chatbot */}
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

      {/* Bottom Controls */}
      <div className="absolute bottom-0 left-0 right-0 bg-blue-600 text-white p-4 flex justify-center space-x-4">
        <button className="px-4 py-2 bg-white text-blue-600 rounded-lg shadow hover:bg-gray-100">
          Buy
        </button>
        <button className="px-4 py-2 bg-white text-blue-600 rounded-lg shadow hover:bg-gray-100">
          Sell
        </button>
        <select className="px-3 py-2 rounded-md text-blue-600">
          <option value="">Investor Principles</option>
          <option>Goal Setting</option>
          <option>Rebalancing</option>
          <option>Risk Tolerance</option>
          <option>Long-Term Thinking</option>
        </select>
      </div>
    </div>
  );
}
