import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Hand, Home, Accessibility, Languages, Contrast, Moon, Sun, Type, Eye, ZoomIn, X } from 'lucide-react';
import React, { useState, useEffect, createContext, useContext } from 'react';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import About from './components/About';
import History from './components/History';

export const AppContext = createContext();

function Navigation() {
  const location = useLocation();
  const { lang, setLang, theme, setTheme, highContrast, setHighContrast } = useContext(AppContext);
  
  const translations = {
    en: { home: 'Home', dashboard: 'Dashboard', about: 'About', title: 'SignVoice AI' },
    hi: { home: 'होम', dashboard: 'डैशबोर्ड', about: 'हमारे बारे में', title: 'साइनवॉइस एआई' }
  };
  const t = translations[lang];

  return (
    <nav style={{ 
      borderBottom: '1px solid var(--glass-border)', 
      padding: '20px 0', 
      background: theme === 'light' ? 'rgba(255, 255, 255, 0.8)' : 'rgba(10, 10, 11, 0.7)',
      backdropFilter: 'blur(16px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      transition: 'all 0.3s'
    }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '12px', textDecoration: 'none' }}>
          <div style={{ color: 'var(--primary-accent)', display: 'flex', filter: 'drop-shadow(0 0 8px rgba(6, 182, 212, 0.6))' }}>
            <Hand size={28} />
          </div>
          <h1 style={{ margin: 0, fontSize: '1.5rem', color: 'var(--text-main)', letterSpacing: '-0.03em' }}>
            {t.title}
          </h1>
        </Link>
        
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '24px', marginRight: '24px', color: 'var(--text-muted)', fontSize: '0.95rem' }}>
            <Link to="/" style={{ color: location.pathname === '/' ? 'var(--text-main)' : 'var(--text-muted)', textDecoration: 'none', fontWeight: 500, transition: 'color 0.3s' }}>{t.home}</Link>
            <Link to="/dashboard" style={{ color: location.pathname === '/dashboard' ? 'var(--text-main)' : 'var(--text-muted)', textDecoration: 'none', fontWeight: 500, transition: 'color 0.3s' }}>{t.dashboard}</Link>
            <Link to="/about" style={{ color: location.pathname === '/about' ? 'var(--text-main)' : 'var(--text-muted)', textDecoration: 'none', fontWeight: 500, transition: 'color 0.3s' }}>{t.about}</Link>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={() => setLang(lang === 'en' ? 'hi' : 'en')} className="btn-glass" style={{ padding: '8px', borderRadius: '8px', cursor: 'pointer', background: 'var(--glass-bg)', color: 'var(--text-main)', border: '1px solid var(--glass-border)' }} title="Toggle Language">
              <span style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>{lang === 'en' ? 'HI' : 'EN'}</span>
            </button>
            <button onClick={() => setHighContrast(!highContrast)} className="btn-glass" style={{ padding: '8px', borderRadius: '8px', cursor: 'pointer', background: highContrast ? 'var(--glass-hover)' : 'var(--glass-bg)', color: 'var(--text-main)', border: '1px solid var(--glass-border)' }} title="High Contrast">
              <Contrast size={18} color={highContrast ? "var(--primary-accent)" : "currentColor"} />
            </button>
            <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} className="btn-glass" style={{ padding: '8px', borderRadius: '8px', cursor: 'pointer', background: 'var(--glass-bg)', color: 'var(--text-main)', border: '1px solid var(--glass-border)' }} title="Toggle Theme">
              {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  const [accessOpen, setAccessOpen] = useState(false);
  const [highContrast, setHighContrast] = useState(false);
  const [largeText, setLargeText] = useState(false);
  const [dyslexiaFont, setDyslexiaFont] = useState(false);
  const [theme, setTheme] = useState('dark');
  const [lang, setLang] = useState('en');

  useEffect(() => {
    if (highContrast) document.body.classList.add('high-contrast');
    else document.body.classList.remove('high-contrast');
    
    if (largeText) document.body.classList.add('large-text');
    else document.body.classList.remove('large-text');
    
    if (dyslexiaFont) document.body.classList.add('dyslexia-font');
    else document.body.classList.remove('dyslexia-font');

    if (theme === 'light') document.body.classList.add('light-theme');
    else document.body.classList.remove('light-theme');

    document.documentElement.lang = lang;
  }, [highContrast, largeText, dyslexiaFont, theme, lang]);

  return (
    <AppContext.Provider value={{ lang, setLang, theme, setTheme, highContrast, setHighContrast }}>
      <Router>
        <Navigation />
        
        <main className="main-content container">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/about" element={<About />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
        
        <footer style={{ borderTop: '1px solid var(--glass-border)', padding: '32px 0', textAlign: 'center', color: 'var(--text-muted)', marginTop: 'auto' }}>
          <p style={{ margin: 0, fontSize: '0.9rem' }}>© {new Date().getFullYear()} SignVoice AI. All rights reserved. Connecting worlds together.</p>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '16px' }}>
            <span style={{ cursor: 'pointer' }}>GitHub</span>
            <span style={{ cursor: 'pointer' }}>Twitter</span>
            <span style={{ cursor: 'pointer' }}>LinkedIn</span>
          </div>
        </footer>

        {/* Accessibility Menu */}
        {accessOpen && (
          <div className="card" style={{
            position: 'fixed',
            bottom: '100px',
            right: '24px',
            width: '280px',
            padding: '24px',
            zIndex: 101,
            animation: 'fadeIn 0.2s ease-out'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h3 style={{ margin: 0, fontSize: '1.2rem' }}>Accessibility</h3>
              <button onClick={() => setAccessOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <button 
                onClick={() => setHighContrast(!highContrast)}
                className="btn btn-outline" 
                style={{ justifyContent: 'flex-start', background: highContrast ? 'var(--glass-hover)' : 'transparent', borderColor: highContrast ? 'var(--primary-accent)' : 'var(--glass-border)' }}
              >
                <Eye size={18} /> High Contrast
              </button>
              <button 
                onClick={() => setLargeText(!largeText)}
                className="btn btn-outline" 
                style={{ justifyContent: 'flex-start', background: largeText ? 'var(--glass-hover)' : 'transparent', borderColor: largeText ? 'var(--primary-accent)' : 'var(--glass-border)' }}
              >
                <ZoomIn size={18} /> Larger Text
              </button>
              <button 
                onClick={() => setDyslexiaFont(!dyslexiaFont)}
                className="btn btn-outline" 
                style={{ justifyContent: 'flex-start', background: dyslexiaFont ? 'var(--glass-hover)' : 'transparent', borderColor: dyslexiaFont ? 'var(--primary-accent)' : 'var(--glass-border)' }}
              >
                <Type size={18} /> Dyslexia Font
              </button>
            </div>
          </div>
        )}

        <button onClick={() => setAccessOpen(!accessOpen)} className="fab-access shadow-glow" aria-label="Accessibility Options">
          <Accessibility size={24} />
        </button>
      </Router>
    </AppContext.Provider>
  );
}

export default App;
