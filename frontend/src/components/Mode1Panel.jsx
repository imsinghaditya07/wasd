import React, { useEffect, useRef, useState } from 'react';
import { Camera, Volume2, AlertCircle } from 'lucide-react';
// import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision';

export default function Mode1Panel() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isActive, setIsActive] = useState(false);
  const [currentWord, setCurrentWord] = useState('Waiting...');
  const [confidence, setConfidence] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  // We define the Web Speech API TTS
  const speakWord = () => {
    if (currentWord && currentWord !== 'Waiting...' && currentWord !== 'No hand detected') {
      const utterance = new SpeechSynthesisUtterance(currentWord);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  };

  const startCamera = async () => {
    try {
      setIsLoading(true);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: true 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play();
          setIsActive(true);
          setIsLoading(false);
          // In a real app, instantiate MediaPipe here and requestAnimationFrame loop
        };
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      let errorMsg = 'Camera Error';
      
      if (err.name === 'NotAllowedError' || err.message.includes('Permission denied')) {
        errorMsg = 'Permission Denied: Please click the lock icon next to your URL bar and allow Camera access.';
      } else if (err.name === 'NotFoundError' || err.message.includes('Requested device not found')) {
        errorMsg = 'No Camera Found: Please make sure your laptop webcam is connected.';
      } else if (err.name === 'NotReadableError' || err.message.includes('hardware error')) {
        errorMsg = 'Camera Blocked: Another app (like Zoom/Teams or Python) is using your camera right now. Close them and try again.';
      }
      
      setCurrentWord(errorMsg);
      setIsLoading(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(t => t.stop());
      videoRef.current.srcObject = null;
    }
    setIsActive(false);
    setCurrentWord('Waiting...');
    setConfidence(0);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2 style={{ color: 'var(--primary-blue)', margin: 0 }}>Sign → Speech (Mode 1)</h2>
          <p style={{ margin: 0, color: '#6B7280' }}>Uses webcam to track gestures and reads them aloud.</p>
        </div>
        <div>
          {!isActive ? (
            <button className="btn btn-primary" onClick={startCamera} disabled={isLoading}>
              <Camera size={18} />
              {isLoading ? 'Starting...' : 'Start Camera'}
            </button>
          ) : (
            <button className="btn btn-outline" onClick={stopCamera}>
              Stop Camera
            </button>
          )}
        </div>
      </div>

      <div className="video-container">
        {!isActive && !isLoading && (
          <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'gray' }}>
            <Camera size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
            <p>Camera is paused. Click Start Camera.</p>
          </div>
        )}
        <video 
          ref={videoRef}
          className="video-feed" 
          playsInline
        />
        <canvas 
          ref={canvasRef}
          className="video-canvas"
        />
        {isActive && (
          <div className="video-overlay">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div className="pulse-dot"></div>
              <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>LIVE WEBCAM PREDICTION</span>
            </div>
          </div>
        )}
      </div>

      <div style={{ marginTop: '32px', textAlign: 'center' }}>
        <h3 style={{ fontSize: '1rem', textTransform: 'uppercase', letterSpacing: '1px', color: '#6B7280' }}>Detected Sign</h3>
        <div style={{ fontSize: '3rem', fontWeight: 700, color: 'var(--dark-text)', margin: '16px 0', textTransform: 'capitalize' }}>
          {currentWord}
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '24px' }}>
          <span style={{ fontWeight: 600 }}>Confidence:</span>
          <div style={{ width: '200px', height: '10px', background: 'var(--light-gray)', borderRadius: '5px', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${confidence}%`, background: 'var(--primary-blue)', transition: 'width 0.2s' }}></div>
          </div>
          <span>{confidence.toFixed(0)}%</span>
        </div>

        <button 
          className="btn btn-primary" 
          onClick={speakWord} 
          disabled={!isActive || currentWord === 'Waiting...' || currentWord === 'No hand detected'}
          style={{ width: '200px', height: '54px', fontSize: '1.1rem' }}
        >
          <Volume2 size={24} />
          Speak Word
        </button>
      </div>
      
      <div style={{ marginTop: '32px', padding: '16px', background: 'var(--secondary-blue)', borderRadius: '8px', display: 'flex', gap: '12px' }}>
        <AlertCircle color="var(--primary-blue)" />
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#1E3A8A' }}>
          <strong>Note:</strong> In a full deployment, TensorFlow.js and MediaPipe Hands are injected here to perform the 30-frame sequence prediction entirely in your browser using the exact same logic as your Python application.
        </p>
      </div>
    </div>
  );
}
