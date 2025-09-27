import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const menuItems = [
    { name: "Portfolio Management", path: "/portfolio" },
    { name: "Investor Principles", path: "/investor" }
  ];

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-1/4 bg-white shadow-md p-6 flex flex-col">
        <h2 className="text-xl font-bold mb-6">Investor Principles</h2>
        <ul className="space-y-3">
          {menuItems.map((item) => (
            <li key={item.path}>
              <button
                onClick={() => navigate(item.path)}
                className="w-full text-left p-3 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {item.name}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      <main className="flex-1 p-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Educational Social Media Stock Trading
        </h1>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl">
          Teach financially illiterate people investor principles in a fun way,
          using social media and music streaming data as "stocks." Earn rewards
          while learning!
        </p>

        <div className="grid grid-cols-2 gap-6 mt-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="font-semibold text-lg mb-3">Featured Lesson</h3>
            <p>Learn the basics of portfolio management</p>
            <button
              onClick={() => navigate('/portfolio')}
              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Start Learning
            </button>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="font-semibold text-lg mb-3">Quick Quiz</h3>
            <p>Test your investment knowledge</p>
            <button
              onClick={() => navigate('/quiz')}
              className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Take Quiz
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}