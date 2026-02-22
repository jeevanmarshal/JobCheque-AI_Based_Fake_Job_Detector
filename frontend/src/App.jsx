import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ReportScam from './pages/ReportScam';
import Awareness from './pages/Awareness';

function App() {
  return (
    <Router>
      <div className="main-container">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/report" element={<ReportScam />} />
          <Route path="/awareness" element={<Awareness />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
