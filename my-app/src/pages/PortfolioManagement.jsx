import { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function PortfolioManagement() {
  const [channels, setChannels] = useState([]);
  const [selectedChannel, setSelectedChannel] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [channelData, setChannelData] = useState([]); // holds chart data

  // Fetch channels from backend
  useEffect(() => {
    async function fetchChannels() {
      try {
        const response = await fetch(
          `http://localhost:5000/get-yt-channels-and-views/`
        );
        const data = await response.json();
        setChannels(data);
        if (data.length > 0) setSelectedChannel(data[0].name);
      } catch (error) {
        console.error("Error fetching channels:", error);
      }
    }

    fetchChannels();
  }, []);

  // Update chart data when selected channel changes
  useEffect(() => {
    if (!selectedChannel) return;
    const channel = channels.find((c) => c.name === selectedChannel);
    if (channel) {
      // Example: generate 7 days of views with slight random variation
      const data = Array.from({ length: 7 }, (_, i) =>
        Math.floor(channel.views * (0.9 + Math.random() * 0.2))
      );
      setChannelData(data);
    }
  }, [selectedChannel, channels]);

  // Filter channels by search query
  const filteredChannels = channels.filter((channel) =>
    channel.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Chart.js config
  const chartData = {
    labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
    datasets: [
      {
        label: `${selectedChannel} Views`,
        data: channelData,
        borderColor: "rgba(37, 99, 235, 1)",
        backgroundColor: "rgba(37, 99, 235, 0.2)",
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Top 50 Videos Time vs. Views',
        front: {
          size: 18
        }
      },
    },
    scales: {
      x: {
        reverse: true,
        title: {
          display: true,
          text: 'Time'
        },
        beginAtZero: false,
        ticks: {
          callback: function (value, index, ticks) {
            return value + " day(s)"
          }
        }
      },
      y: {
        title: {
          display: true,
          text: 'Views'
        },
        beginAtZero: true,
        ticks: {
          callback: function (value, index, ticks) {
            return value + ' mill';
          }
        }
      }
    },
  };

  return (
    <div className="flex min-h-screen bg-gray-100 p-6 gap-6">
      {/* Left Sidebar */}
      <div className="w-1/4 bg-white shadow-lg rounded-xl p-6 flex flex-col">
        <h2 className="text-xl font-bold mb-6">📊 Portfolio</h2>
        <ul className="space-y-3">
          <li className="flex justify-between border-b border-gray-200 pb-2 text-gray-800 font-medium hover:bg-gray-50 rounded-md px-2 transition">
            <span>YouTube Music</span>
            <span>$250</span>
          </li>
          <li className="flex justify-between border-b border-gray-200 pb-2 text-gray-800 font-medium hover:bg-gray-50 rounded-md px-2 transition">
            <span>TikTok Trends</span>
            <span>$150</span>
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <main className="flex-1 flex flex-col gap-6">
        <h1 className="text-2xl font-bold mb-4">Market Dashboard</h1>

        <div className="flex gap-6 flex-1">
          {/* Chart Section */}
          <div className="flex-1 flex flex-col gap-4">
            {/* Search Input */}
            <input
              type="text"
              placeholder="Search for a channel..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="p-3 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 transition mb-2"
            />

            {/* Dropdown */}
            <select
              value={selectedChannel}
              onChange={(e) => setSelectedChannel(e.target.value)}
              className="p-3 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 transition mb-2"
            >
              {filteredChannels.map((channel) => (
                <option key={channel.name} value={channel.name}>
                  {channel.name} - {channel.views.toLocaleString()} views
                </option>
              ))}
            </select>

            {/* Chart / Channel Info */}
            <div className="bg-white rounded-xl shadow-lg p-6 h-96 flex flex-col gap-4">
              {/* Chart.js Canvas */}
              <div className="flex-1">
                {selectedChannel && <Line data={chartData} options={chartOptions} />}
              </div>

              {/* Channel Info */}
              {filteredChannels
                .filter((c) => c.name === selectedChannel)
                .map((channel) => (
                  <div
                    key={channel.name}
                    className="flex justify-between w-full border-b border-gray-200 pb-1 text-gray-800 font-medium"
                  >
                    <span>{channel.name}</span>
                    <span>{channel.views.toLocaleString()} views</span>
                  </div>
                ))}
            </div>
          </div>

          {/* AI Chat Section */}
          <aside className="w-1/3 bg-white shadow-lg rounded-xl p-6 flex flex-col gap-4">
            <h2 className="text-xl font-bold mb-2">🤖 Chatbot</h2>
            <div className="flex-1 bg-gray-50 p-4 rounded-md text-gray-600 overflow-y-auto">
              <p>AI Assistant is here to help</p>
            </div>
            <input
              type="text"
              placeholder="Ask anything..."
              className="mt-2 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            />
          </aside>
        </div>
      </main>
    </div>
  );
}
