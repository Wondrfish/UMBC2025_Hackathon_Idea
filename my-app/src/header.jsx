import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1
          onClick={() => navigate("/investor")}
          className="text-2xl font-bold cursor-pointer hover:text-blue-200 transition"
        >
          Investor Portfolio
        </h1>
        <nav>
          <button
            onClick={() => navigate("/")}
            className="mx-2 hover:text-blue-200 transition"
          >
            Home
          </button>
        </nav>
      </div>
    </header>
  );
}
