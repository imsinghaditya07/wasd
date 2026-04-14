// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import './index.css';

// Professional Core SVG Icons
const CameraIcon = () => (
  <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
    <circle cx="12" cy="13" r="4"></circle>
  </svg>
);

const MicIcon = () => (
  <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
    <line x1="12" y1="19" x2="12" y2="22"></line>
  </svg>
);

const BackIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 18l-6-6 6-6"/>
  </svg>
);

function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check initial user preference natively or fallback to light
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setIsDark(true);
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = !isDark;
    setIsDark(nextTheme);
    if (nextTheme) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  };

  return (
    <div className="top-controls">
      <span style={{ fontSize: '0.86rem', fontWeight: 500, color: 'var(--text-light)', userSelect: 'none' }}>
        {isDark ? 'Dark Mode' : 'Light Mode'}
      </span>
      <label className="theme-switch" aria-label="Toggle Theme">
        <input type="checkbox" checked={isDark} onChange={toggleTheme} />
        <span className="slider"></span>
      </label>
    </div>
  );
}

function Mode1Translator({ onBack }) {
  const [status, setStatus] = useState({ current_word: "Connecting...", confidence: 0 });
  const [imgError, setImgError] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://localhost:5000/status')
        .then(res => res.json())
        .then(data => {
          setStatus(data);
          setImgError(false);
        })
        .catch(err => {
          setStatus({ current_word: "Server Offline", confidence: 0 });
        });
    }, 150);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-panel">
      <ThemeToggle />
      <button className="back-button" onClick={onBack}>
        <BackIcon /> Menu
      </button>
      
      <div style={{ marginTop: '20px' }}>
        <h1>Sign to Speech</h1>
        <p className="subtitle">Real-time dynamic gesture recognition.</p>
        
        <div className="video-container">
          {imgError ? (
            <p style={{ color: 'var(--text-light)', fontWeight: 500 }}>Waiting for Camera Feed...</p>
          ) : (
            <img 
              src="http://localhost:5000/video_feed" 
              alt="Live Camera Feed"
              className="video-feed"
              onError={() => setImgError(true)}
            />
          )}
        </div>

        <div className="status-dashboard">
          <div className="prediction-box">
            <span className="label">Live Translation</span>
            <span className="word-output">{status.current_word}</span>
          </div>
          
          <div className="prediction-box" style={{ alignItems: 'flex-end' }}>
            <span className="label">Confidence</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginTop: '8px' }}>
              <span style={{ fontWeight: 600, fontSize: '1.1rem', color: 'var(--primary-blue)' }}>
                {Math.round(status.confidence * 100)}%
              </span>
              <div className="progress-container">
                <div 
                  className="progress-bar" 
                  style={{ width: `${Math.round(status.confidence * 100)}%` }} 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Mode2Translator({ onBack }) {
  return (
    <div className="glass-panel">
      <ThemeToggle />
      <button className="back-button" onClick={onBack}>
        <BackIcon /> Menu
      </button>
      
      <div style={{ marginTop: '20px' }}>
        <h1>Speech to Sign</h1>
        <p className="subtitle">Speak into the microphone to see corresponding signs.</p>
        
        <div className="video-container" style={{ minHeight: '350px', background: 'var(--dashboard-bg)', border: `2px dashed var(--border-color)` }}>
            <div style={{ textAlign: 'center', color: 'var(--text-light)' }}>
              <MicIcon />
              <p style={{ fontWeight: 500, marginTop: '20px', fontSize: '1.1rem' }}>
                Microphone Integration Coming Soon...
              </p>
            </div>
        </div>
      </div>
    </div>
  );
}

function LandingPage({ onNavigate }) {
  return (
    <div className="glass-panel" style={{ background: 'transparent', boxShadow: 'none', border: 'none', maxWidth: '800px' }}>
      <ThemeToggle />
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ fontSize: '3.6rem', fontWeight: 700, marginBottom: '8px' }}>SilentBridge</h1>
        <p className="subtitle" style={{ fontSize: '1.25rem', marginBottom: '60px' }}>
          Bi-Directional Sign Language Translator
        </p>
      </div>
      
      <div className="cards-container">
        <div className="mode-card" onClick={() => onNavigate('mode1')}>
          <div className="card-icon"><CameraIcon /></div>
          <div className="card-title">Sign to Speech</div>
          <div className="card-desc">Use your webcam to effortlessly translate dynamic sign language into spoken text in real time.</div>
        </div>

        <div className="mode-card" onClick={() => onNavigate('mode2')}>
          <div className="card-icon"><MicIcon /></div>
          <div className="card-title">Speech to Sign</div>
          <div className="card-desc">Speak into your microphone and view the corresponding sign language animations instantly.</div>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  return (
    <>
      {currentPage === 'landing' && <LandingPage onNavigate={setCurrentPage} />}
      {currentPage === 'mode1' && <Mode1Translator onBack={() => setCurrentPage('landing')} />}
      {currentPage === 'mode2' && <Mode2Translator onBack={() => setCurrentPage('landing')} />}
    </>
  );
}

export default App;
