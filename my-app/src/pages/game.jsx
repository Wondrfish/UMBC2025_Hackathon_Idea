import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-1/4 bg-white shadow-md p-6 flex flex-col">
        <h2 className="text-xl font-bold mb-4">Investor Principles</h2>
        <ul className="space-y-2 text-gray-700">
          <li>Portfolio Management</li>
          <li>Goal Setting</li>
          <li>Rebalancing</li>
          <li>Risk Tolerance</li>
          <li>Long-Term Thinking</li>
        </ul>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Educational Social Media Betting
        </h1>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl">
          Teach financially illiterate people investor principles in a fun way,
          using social media and music streaming data as "stocks." Earn rewards
          while learning!
        </p>

        {/* Target Prizes */}
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🎁 Target Prizes</h2>
          <p className="text-gray-700">T. Rowe Price, Education, AI</p>
        </div>

        {/* Team Contributions */}
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">👩‍💻 Team Contributions</h2>
          <ul className="list-disc list-inside space-y-1 text-gray-700">
            <li><strong>Ajani:</strong> YouTube API + storing in DB</li>
            <li><strong>Elizabeth:</strong> Querying DB + Chart.js</li>
            <li><strong>Kristina:</strong> Gemini API chatbot</li>
            <li><strong>T:</strong> UI/Frontend + investor principles dropdown</li>
          </ul>
        </div>

        {/* Call-to-action */}
        <button
          onClick={() => navigate("/game")}
          className="px-6 py-3 bg-blue-600 text-white rounded-xl shadow hover:bg-blue-700 transition"
        >
          🚀 Start the Game
        </button>
      </main>
    </div>

  );

}

