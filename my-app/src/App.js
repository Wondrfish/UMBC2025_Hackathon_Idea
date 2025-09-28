import './App.css';
import React, {useState, UseEffect} from 'react'
import Home from "./pages/home";
import Game from "./pages/game";
import PortfolioManagement from "./pages/PortfolioManagement";
import InvestorPrinciples from "./pages/InvestorPrinciples";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


function App() {
  return (
    <div className="App">
      <header className="App-header">
<Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game" element={<Game />} />
          <Route path="/portfolio" element={<PortfolioManagement />} />
        <Route path="/investor" element={<InvestorPrinciples />} />
      </Routes>
    </Router>
      </header>
    </div>
  );
}

export default App;
