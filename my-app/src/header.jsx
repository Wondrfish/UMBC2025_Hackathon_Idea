import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="bg-blue-600 text-white p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <h1
          onClick={() => navigate('/')}
          className="text-2xl font-bold cursor-pointer hover:text-blue-200"
        >
          EduInvest
        </h1>
        <nav>
          <button
            onClick={() => navigate('/')}
            className="mx-2 hover:text-blue-200"
          >
            Home
          </button>
        </nav>
      </div>
    </header>
  );
}