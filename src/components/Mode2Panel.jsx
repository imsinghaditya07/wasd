import React, { useState, useRef } from 'react';
import { Mic, MicOff, RefreshCw, AlertCircle } from 'lucide-react';

export default function Mode2Panel() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [displayWord, setDisplayWord] = useState('');
  const [gifUrl, setGifUrl] = useState('');
  
  // Fake dictionary simply mapped for demonstration of the concept
  const dictionary = {
    'hello': 'https://www.lifeprint.com/asl101/gifs/h/hello.gif',
    'help': 'https://www.lifeprint.com/asl101/gifs/h/help.gif',
    'thank you': 'https://www.lifeprint.com/asl101/gifs/t/thankyou.gif',
    'please': 'https://www.lifeprint.com/asl101/gifs/p/please.gif',
    'water': 'https://www.lifeprint.com/asl101/gifs/w/water.gif'
  };

  const recognitionRef = useRef(null);

  const startListening = () => {
    // Setup Web Speech API for Speech to Text
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Your browser does not support Speech Recognition. Please use Chrome.");
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.continuous = false;
    recognitionRef.current.interimResults = false;
    recognitionRef.current.lang = 'en-US';

    recognitionRef.current.onstart = () => {
      setIsListening(true);
      setTranscript('Listening...');
      setGifUrl('');
      setDisplayWord('');
    };

    recognitionRef.current.onresult = (event) => {
      const result = event.results[0][0].transcript.toLowerCase().trim();
      setTranscript(`You said: "${result}"`);
      processWord(result);
    };

    recognitionRef.current.onerror = (event) => {
      console.error("Speech error", event.error);
      setTranscript(`Error: ${event.error}`);
      setIsListening(false);
    };

    recognitionRef.current.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current.start();
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  };

  const processWord = (word) => {
    // Simplified mapping logic
    let matchedWord = null;
    
    if (dictionary[word]) {
      matchedWord = word;
    } else {
      // Very basic fuzzy search logic placeholder
      Object.keys(dictionary).forEach(key => {
        if (word.includes(key)) matchedWord = key;
      });
    }

    if (matchedWord) {
      setDisplayWord(matchedWord);
      setGifUrl(dictionary[matchedWord]);
    } else {
      setDisplayWord('Sign not found');
      setGifUrl('https://upload.wikimedia.org/wikipedia/commons/c/ce/Transparent.gif');
    }
  };

  return (
    <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2 style={{ color: 'var(--primary-blue)', margin: 0 }}>Speech → Sign (Mode 2)</h2>
          <p style={{ margin: 0, color: '#6B7280' }}>Uses your microphone to listen and outputs ASL signs.</p>
        </div>
        <div>
          {!isListening ? (
            <button className="btn btn-primary" onClick={startListening}>
              <Mic size={18} />
              Start Listening
            </button>
          ) : (
            <button className="btn btn-outline" onClick={stopListening} style={{ color: '#EF4444', borderColor: '#EF4444' }}>
              <MicOff size={18} />
              Stop
            </button>
          )}
        </div>
      </div>

      <div style={{ display: 'flex', gap: '32px', minHeight: '300px' }}>
        {/* Left Col: Status */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ padding: '24px', background: 'var(--light-gray)', borderRadius: '12px', flex: 1 }}>
            <h3 style={{ fontSize: '0.9rem', textTransform: 'uppercase', color: '#6B7280', letterSpacing: '1px' }}>Microphone Status</h3>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '12px', 
              marginTop: '16px',
              color: isListening ? 'var(--success-color)' : 'var(--dark-text)' 
            }}>
              {isListening ? <RefreshCw className="pulse-dot" size={24} style={{ background: 'none', animation: 'spin 2s linear infinite' }} /> : <MicOff size={24} />}
              <span style={{ fontSize: '1.2rem', fontWeight: 500 }}>
                {isListening ? 'Recording Audio...' : 'Idle'}
              </span>
            </div>

            <div style={{ marginTop: '32px' }}>
               <h3 style={{ fontSize: '0.9rem', textTransform: 'uppercase', color: '#6B7280', letterSpacing: '1px' }}>Transcript</h3>
               <p style={{ fontSize: '1.2rem', fontStyle: 'italic', marginTop: '8px' }}>
                 {transcript || 'Press Start Listening and say "hello" or "thank you".'}
               </p>
            </div>
          </div>
        </div>

        {/* Right Col: GIF Display */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', border: '2px dashed var(--border-color)', borderRadius: '12px', padding: '20px' }}>
          {gifUrl ? (
            <>
              <img 
                src={gifUrl} 
                alt={displayWord} 
                style={{ width: '100%', maxHeight: '250px', objectFit: 'contain', borderRadius: '8px' }} 
              />
              <h3 style={{ marginTop: '16px', fontSize: '1.5rem', color: 'var(--primary-blue)', textTransform: 'uppercase' }}>
                {displayWord}
              </h3>
            </>
          ) : (
             <div style={{ textAlign: 'center', color: '#9CA3AF' }}>
               <AlertCircle size={48} style={{ margin: '0 auto', marginBottom: '16px', opacity: 0.5 }} />
               <p>Sign will appear here</p>
             </div>
          )}
        </div>
      </div>
    </div>
  );
}
