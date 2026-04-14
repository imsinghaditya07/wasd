import React, { useState, useRef, useEffect } from 'react';
import { Camera, Volume2, Mic, MicOff, RefreshCw, AlertCircle, Clock, Video, VideoOff, RefreshCcw, Hand, Activity, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('sign'); // 'sign' or 'speech'
  
  // Backend State
  const [currentWord, setCurrentWord] = useState('Waiting...');
  const [confidence, setConfidence] = useState(0);
  const [isBackendLive, setIsBackendLive] = useState(false);
  const [history, setHistory] = useState([]);

  // Mode 2 State (Speech -> Sign)
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [displaySign, setDisplaySign] = useState(null);
  const recognitionRef = useRef(null);

  // Fake Dictionary for Mode 2
  const dictionary = {
    'hello': 'https://www.lifeprint.com/asl101/gifs/h/hello.gif',
    'thank you': 'https://www.lifeprint.com/asl101/gifs/t/thankyou.gif',
    'good morning': 'https://www.lifeprint.com/asl101/gifs/g/good-morning.gif',
    'yes': 'https://www.lifeprint.com/asl101/gifs/y/yes.gif',
    'no': 'https://www.lifeprint.com/asl101/gifs/n/no.gif',
  };

  // --- Backend Polling ---
  useEffect(() => {
    let pollInterval;
    if (activeTab === 'sign') {
      pollInterval = setInterval(async () => {
        try {
          const res = await fetch('/status');
          const data = await res.json();
          setCurrentWord(data.current_word);
          setConfidence(data.confidence);
          setIsBackendLive(true);

          if (data.current_word && data.current_word !== 'Waiting...' && data.current_word !== 'Ready (No hand)' && data.current_word !== 'Analyzing...' && !data.current_word.includes('Recording')) {
              // Add to history if unique
              setHistory(prev => {
                  if (prev[0]?.word === data.current_word) return prev;
                  return [{word: data.current_word, time: new Date().toLocaleTimeString()}, ...prev].slice(0, 10);
              });
          }
        } catch (err) {
          setIsBackendLive(false);
        }
      }, 500);
    }
    return () => clearInterval(pollInterval);
  }, [activeTab]);

  // --- Mode 2 Logic ---
  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.lang = 'en-US';
    
    recognitionRef.current.onstart = () => {
      setIsListening(true);
      setTranscript('Listening...');
      setDisplaySign(null);
    };
    recognitionRef.current.onresult = (e) => {
      const result = e.results[0][0].transcript.toLowerCase().trim();
      setTranscript(result);
      let match = null;
      Object.keys(dictionary).forEach(key => {
        if (result.includes(key)) match = key;
      });
      if (match) setDisplaySign(dictionary[match]);
    };
    recognitionRef.current.onend = () => setIsListening(false);
    recognitionRef.current.start();
  };

  const stopListening = () => {
    if (recognitionRef.current) recognitionRef.current.stop();
    setIsListening(false);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out' }}>
      
      {/* Dashboard Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '8px', letterSpacing: '-0.04em' }}>
            Live <span className="text-gradient">Dashboard</span>
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>Real-time interpretation & bridge communication</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
             <div className={`card ${isBackendLive ? 'shadow-glow' : ''}`} style={{ padding: '8px 16px', borderRadius: '100px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px', background: isBackendLive ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderColor: isBackendLive ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)' }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: isBackendLive ? '#10b981' : '#ef4444' }}></div>
                {isBackendLive ? 'Engine: ONLINE' : 'Engine: OFFLINE'}
             </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '40px', background: 'rgba(255,255,255,0.02)', padding: '6px', borderRadius: '20px', display: 'inline-flex', border: '1px solid var(--glass-border)' }}>
        <button 
          onClick={() => { setActiveTab('sign'); stopListening(); }}
          style={{
            padding: '12px 28px',
            borderRadius: '16px',
            border: 'none',
            cursor: 'pointer',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            background: activeTab === 'sign' ? 'var(--primary-gradient)' : 'transparent',
            color: activeTab === 'sign' ? '#fff' : 'var(--text-muted)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: activeTab === 'sign' ? '0 4px 15px rgba(6, 182, 212, 0.3)' : 'none'
          }}
        >
          <Hand size={18} /> Sign ➔ Speech
        </button>

        <button 
          onClick={() => { setActiveTab('speech'); }}
          style={{
            padding: '12px 28px',
            borderRadius: '16px',
            border: 'none',
            cursor: 'pointer',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            background: activeTab === 'speech' ? 'var(--primary-gradient)' : 'transparent',
            color: activeTab === 'speech' ? '#fff' : 'var(--text-muted)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: activeTab === 'speech' ? '0 4px 15px rgba(6, 182, 212, 0.3)' : 'none'
          }}
        >
          <Mic size={18} /> Speech ➔ Sign
        </button>
      </div>

      {/* Content Area */}
      <div style={{ display: 'flex', gap: '32px', flexDirection: 'column' }}>
        
        {activeTab === 'sign' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '32px' }}>
            {/* Viewport Area */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              <div className="card" style={{ padding: '0', overflow: 'hidden', minHeight: '500px', position: 'relative', border: '1px solid rgba(255,255,255,0.1)' }}>
                <div style={{ position: 'absolute', top: 24, left: 24, zIndex: 10, display: 'flex', gap: 12 }}>
                    <div style={{ background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(8px)', padding: '6px 14px', borderRadius: '100px', fontSize: '0.75rem', fontWeight: 600, color: 'white', border: '1px solid rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div className="pulse-dot"></div> ACTIVE FEED
                    </div>
                </div>

                {isBackendLive ? (
                   <img src="/video_feed" alt="Video Feed" style={{ width: '100%', height: '500px', objectFit: 'cover', background: '#000' }} />
                ) : (
                  <div style={{ width: '100%', height: '500px', background: '#0a0a0b', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
                    <VideoOff size={64} style={{ marginBottom: 20, opacity: 0.2 }} />
                    <p style={{ fontWeight: 500 }}>Engine Offline</p>
                    <p style={{ fontSize: '0.85rem', opacity: 0.7 }}>Run 'python web_app.py' to start the interpreter</p>
                  </div>
                )}

                <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, background: 'linear-gradient(to top, rgba(0,0,0,0.95), transparent)', padding: '40px 32px 32px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                        <div>
                            <span style={{ color: 'var(--primary-accent)', fontSize: '0.8rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.1em' }}>Detected Gesture</span>
                            <h2 style={{ fontSize: '3rem', margin: 0, letterSpacing: '-0.02em', textShadow: '0 0 20px rgba(6, 182, 212, 0.4)' }}>{currentWord}</h2>
                        </div>
                        {confidence > 0 && (
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ width: '120px', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: 2, marginBottom: 8, overflow: 'hidden' }}>
                                    <div style={{ width: `${confidence * 100}%`, height: '100%', background: 'var(--primary-accent)', boxShadow: '0 0 10px var(--primary-accent)' }}></div>
                                </div>
                                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)' }}>{Math.round(confidence * 100)}% Match</span>
                            </div>
                        )}
                    </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div style={{ display: 'flex', gap: 16 }}>
                 <div className="card" style={{ flex: 1, padding: '20px 24px', display: 'flex', alignItems: 'center', gap: 16 }}>
                    <div style={{ width: 48, height: 48, borderRadius: 12, background: 'rgba(6, 182, 212, 0.1)', color: 'var(--primary-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Hand size={24} />
                    </div>
                    <div>
                        <h4 style={{ margin: 0, fontSize: '1rem' }}>Dual-Hand Mode</h4>
                        <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>Active (126 features)</p>
                    </div>
                 </div>
                 <div className="card" style={{ flex: 1, padding: '20px 24px', display: 'flex', alignItems: 'center', gap: 16 }}>
                    <div style={{ width: 48, height: 48, borderRadius: 12, background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Sparkles size={24} />
                    </div>
                    <div>
                        <h4 style={{ margin: 0, fontSize: '1rem' }}>Stability Grace</h4>
                        <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>10-frame jitter protect</p>
                    </div>
                 </div>
              </div>
            </div>

            {/* Sidebar Stats */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
                <div className="card" style={{ padding: '24px' }}>
                    <h3 style={{ fontSize: '1.1rem', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: 8 }}>
                        <Clock size={18} style={{ color: 'var(--primary-accent)' }} /> History Log
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {history.length > 0 ? history.map((item, idx) => (
                            <div key={idx} style={{ padding: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontWeight: 600 }}>{item.word}</span>
                                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{item.time}</span>
                            </div>
                        )) : (
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textAlign: 'center', padding: '20px 0' }}>No history yet</p>
                        )}
                    </div>
                </div>

                <div className="card" style={{ padding: '24px', background: 'var(--primary-gradient)', border: 'none' }}>
                    <h3 style={{ fontSize: '1.1rem', marginBottom: '12px', color: '#fff' }}>Dataset Status</h3>
                    <p style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.8)', marginBottom: 20 }}>Your model is currently trained on 33 verified signs.</p>
                    <Link to="/about" style={{ display: 'flex', alignItems: 'center', gap: 8, color: '#fff', fontSize: '0.9rem', fontWeight: 700, textDecoration: 'none' }}>
                        View Vocabulary ➔
                    </Link>
                </div>
            </div>
          </div>
        )}

        {activeTab === 'speech' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '32px', animation: 'fadeIn 0.4s ease-out' }}>
            {/* Input Area */}
            <div className="card" style={{ padding: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '500px', justifyContent: 'center' }}>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '240px',
                height: '240px',
                marginBottom: '40px'
              }}>
                <button 
                  onClick={isListening ? stopListening : startListening}
                  style={{
                    width: '140px',
                    height: '140px',
                    borderRadius: '50%',
                    border: 'none',
                    background: isListening ? 'rgba(239, 68, 68, 0.15)' : 'rgba(6, 182, 212, 0.15)',
                    color: isListening ? '#ef4444' : 'var(--primary-accent)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                    boxShadow: isListening ? '0 0 50px rgba(239, 68, 68, 0.3)' : '0 0 40px rgba(6, 182, 212, 0.2)',
                    zIndex: 2,
                    transform: isListening ? 'scale(1.1)' : 'scale(1)'
                  }}
                >
                  {isListening ? <MicOff size={56} /> : <Mic size={56} />}
                </button>
                {isListening && <div style={{ position: 'absolute', width: '240px', height: '240px', borderRadius: '50%', border: '2px solid #ef4444', opacity: 0.3, animation: 'ping 1.5s infinite' }}></div>}
              </div>

              <div style={{ width: '100%', maxWidth: '400px', textAlign: 'center' }}>
                <h4 style={{ color: 'var(--text-muted)', marginBottom: '12px', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Real-time Link</h4>
                <div style={{ padding: '24px', background: 'rgba(0,0,0,0.3)', borderRadius: '16px', border: '1px solid var(--glass-border)' }}>
                    <p style={{ fontSize: '1.4rem', fontWeight: 600, margin: 0 }}>{transcript || "Tap the microphone to speak"}</p>
                </div>
              </div>
            </div>

            {/* Output Area */}
            <div className="card" style={{ padding: '0', display: 'flex', flexDirection: 'column', minHeight: '500px', overflow: 'hidden' }}>
              <div style={{ padding: '24px 24px 0' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '8px', color: 'var(--primary-accent)' }}>Sign Visualization</h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Visual bridge to ASL translation</p>
              </div>
              <div style={{ 
                flex: 1, 
                background: '#0a0a0b', 
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '24px'
              }}>
                {displaySign ? (
                  <img src={displaySign} alt="Sign Output" style={{ maxWidth: '100%', maxHeight: '350px', borderRadius: '24px', border: '2px solid var(--glass-border)' }} />
                ) : (
                  <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                    <AlertCircle size={64} style={{ margin: '0 auto 20px', opacity: 0.1 }} />
                    <p style={{ fontSize: '1.1rem', fontWeight: 500 }}>No Signal</p>
                    <p style={{ fontSize: '0.85rem', opacity: 0.6 }}>Say "Hello", "Thank you", or "Good Morning"</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
