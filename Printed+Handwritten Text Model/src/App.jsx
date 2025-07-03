import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './components/Home';
import About from './components/About';
import Extract from './components/Extract';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Router>
      <div className={darkMode ? 'dark' : ''}>
        <div className="min-h-screen bg-white dark:bg-gray-900 text-black dark:text-white">
          <nav className="bg-gray-100 dark:bg-gray-800 p-4">
            <div className="container mx-auto flex justify-between">
              <div className="text-lg font-bold">
                <Link to="/">Image Processor</Link>
              </div>
              <div>
                <Link to="/" className="mr-4">Home</Link>
                <Link to="/about" className="mr-4">About</Link>
                <Link to="/extract" className="mr-4">Extract</Link>
              </div>
            </div>
          </nav>
          <main className="container mx-auto py-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/extract" element={<Extract />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
