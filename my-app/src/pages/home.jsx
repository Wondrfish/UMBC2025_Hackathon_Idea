import { useNavigate } from "react-router-dom";
import "../App.css"; // <-- custom CSS

export default function Home() {
  const navigate = useNavigate();

  const menuItems = [
    { name: "Portfolio Management", path: "/portfolio" },
    { name: "Investor Principles", path: "/investor" }
  ];

  return (
    <div className="home-container">

      <aside className="sidebar">
        <h2 className="sidebar-title">Menu</h2>
        <ul className="sidebar-list">
          {menuItems.map((item) => (
            <li key={item.path}>
              <button
                onClick={() => navigate(item.path)}
                className="sidebar-button"
              >
                {item.name}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <h1>Educational Social Media Stock Trading</h1>
        <p>
          Teach financially illiterate people investor principles in a fun way,
          using social media and music streaming data as "stocks." Earn rewards
          while learning!
        </p>

        <div className="card">
          <h3>Featured Lesson</h3>
          <p>Learn the basics of portfolio management</p>
          <button onClick={() => navigate("/portfolio")}>
            Start Learning
          </button>
        </div>
      </main>
    </div>
  );
}
