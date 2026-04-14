import React from 'react';
import { Camera, Mic, ArrowRight, Zap, Globe, Shield, Activity, Brain, Users } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '75vh',
      textAlign: 'center',
      animation: 'fadeIn 0.8s ease-out',
      padding: '40px 0'
    }}>
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
          }
          .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.2);
            border-radius: 100px;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--primary-accent);
            margin-bottom: 32px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
          }
          .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 32px;
            width: 100%;
            margin-top: 100px;
            margin-bottom: 100px;
          }
          .stat-item {
            padding: 32px;
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
          }
          .stat-number {
            font-size: 4rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 16px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
          }
          .stat-label {
            color: var(--text-muted);
            font-size: 1.1rem;
            font-weight: 500;
          }
          .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            width: 100%;
            margin-top: 60px;
          }
          .feature-card {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 32px;
            text-align: left;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
          }
          .feature-card:hover {
            border-color: rgba(6, 182, 212, 0.3);
            transform: translateY(-4px);
            background: var(--glass-hover);
          }
          .feature-icon {
            background: rgba(6, 182, 212, 0.1);
            color: var(--primary-accent);
            width: 56px;
            height: 56px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
            transition: transform 0.3s ease;
          }
          .feature-card:hover .feature-icon {
            transform: scale(1.1);
          }
          .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 12px;
            color: var(--text-main);
          }
          .feature-card p {
            color: var(--text-muted);
            margin: 0;
            line-height: 1.6;
          }
          .how-it-works {
            margin-top: 100px;
            text-align: left;
            width: 100%;
          }
          .step-row {
            display: flex;
            align-items: center;
            gap: 32px;
            margin-bottom: 40px;
            padding: 24px;
            background: rgba(255,255,255,0.02);
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.05);
          }
          .step-number {
            font-size: 5rem;
            font-weight: 800;
            color: rgba(255,255,255,0.05);
            line-height: 1;
            position: absolute;
            right: 24px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
          }
        `}
      </style>

      {/* HERO SECTION */}
      <div className="hero-badge">
        <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--primary-accent)', display: 'block', boxShadow: '0 0 10px var(--primary-accent)' }}></span>
        AI-Powered Communication
      </div>

      <h1 style={{ 
        fontSize: 'clamp(3rem, 8vw, 5rem)', 
        lineHeight: 1.1,
        maxWidth: '1000px',
        marginBottom: '24px',
        fontWeight: 800,
        letterSpacing: '-0em'
      }}>
        Bridging Voices <br/>
        <span className="text-gradient">Beyond Silence</span>
      </h1>
      
      <p style={{ 
        fontSize: '1.25rem', 
        color: 'var(--text-muted)', 
        maxWidth: '700px', 
        margin: '0 auto 48px auto',
        lineHeight: 1.6
      }}>
        Breaking barriers between silence and sound. SignVoice AI helps deaf and hard-of-hearing individuals communicate freely with the world.
      </p>

      <div style={{ display: 'flex', gap: '16px', marginBottom: '100px', justifyContent: 'center', flexWrap: 'wrap' }}>
        <Link to="/dashboard" className="btn btn-primary shadow-glow" style={{ padding: '16px 32px', fontSize: '1.125rem' }}>
          <Camera size={20} />
          Start Sign to Speech
          <ArrowRight size={18} style={{ marginLeft: 8 }} />
        </Link>
        <Link to="/dashboard" className="btn btn-outline" style={{ padding: '16px 32px', fontSize: '1.125rem', borderColor: 'var(--primary-accent)', color: 'var(--primary-accent)' }}>
          <Mic size={20} />
          Start Speech to Sign
        </Link>
      </div>

      {/* FEATURES SECTION */}
      <div style={{ width: '100%', textAlign: 'left' }}>
        <div className="hero-badge" style={{ marginBottom: 16 }}>Features</div>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '16px' }}>Built for Real-World Communication</h2>
        <p style={{ maxWidth: 600, fontSize: '1.1rem' }}>Powerful enough for daily use, simple enough for first-time users.</p>
        
        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon" style={{ color: '#3b82f6', background: 'rgba(59, 130, 246, 0.1)' }}>
              <Zap size={28} />
            </div>
            <h3>Real-time Translation</h3>
            <p>Lightning fast, zero-latency inference translating signs to spoken words seamlessly on the edge.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ color: '#06b6d4', background: 'rgba(6, 182, 212, 0.1)' }}>
              <Brain size={28} />
            </div>
            <h3>AI-Powered Recognition</h3>
            <p>State-of-the-art vision models to capture nuanced micro-gestures and facial expressions accurately.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ color: '#10b981', background: 'rgba(16, 185, 129, 0.1)' }}>
              <Activity size={28} />
            </div>
            <h3>Accessible Design</h3>
            <p>Meeting WCAG AAA standards with built-in screen readers, contrast toggles, and legible typography.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon" style={{ color: '#f59e0b', background: 'rgba(245, 158, 11, 0.1)' }}>
              <Globe size={28} />
            </div>
            <h3>Multi-language Support</h3>
            <p>Native support for English and Hindi, easily localized to multiple global sign languages.</p>
          </div>
        </div>
      </div>

      {/* STATISTICS SECTION */}
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-number" style={{ background: 'linear-gradient(to right, #3b82f6, #60a5fa)', WebkitBackgroundClip: 'text' }}>70M+</div>
          <div className="stat-label">Deaf Worldwide</div>
        </div>
        <div className="stat-item">
          <div className="stat-number" style={{ background: 'linear-gradient(to right, #06b6d4, #22d3ee)', WebkitBackgroundClip: 'text' }}>63M</div>
          <div className="stat-label">In India Alone</div>
        </div>
        <div className="stat-item">
          <div className="stat-number" style={{ background: 'linear-gradient(to right, #10b981, #34d399)', WebkitBackgroundClip: 'text' }}>95%</div>
          <div className="stat-label">Lack Assistive Tools</div>
        </div>
      </div>

      {/* HOW IT WORKS SECTION */}
      <div className="how-it-works">
        <div className="hero-badge" style={{ marginBottom: 16 }}>Workflow</div>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '40px' }}>How It Works</h2>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="step-row" style={{ position: 'relative' }}>
            <div style={{ width: 64, height: 64, borderRadius: 32, background: 'rgba(59, 130, 246, 0.2)', color: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Camera size={32} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: 8 }}>Capture</h3>
              <p style={{ margin: 0, color: 'var(--text-muted)' }}>The system utilizes your standard device camera to track continuous hand movements and gestures in real-time.</p>
            </div>
            <div className="step-number">01</div>
          </div>

          <div className="step-row" style={{ position: 'relative' }}>
            <div style={{ width: 64, height: 64, borderRadius: 32, background: 'rgba(6, 182, 212, 0.2)', color: '#06b6d4', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Brain size={32} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: 8 }}>Analyze</h3>
              <p style={{ margin: 0, color: 'var(--text-muted)' }}>Our robust edge AI pipeline processes holistic gesture skeletons and immediately classifies intended words.</p>
            </div>
            <div className="step-number">02</div>
          </div>

          <div className="step-row" style={{ position: 'relative' }}>
            <div style={{ width: 64, height: 64, borderRadius: 32, background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Mic size={32} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: 8 }}>Translate</h3>
              <p style={{ margin: 0, color: 'var(--text-muted)' }}>The recognized gestures are smoothly synthesized into contextual sentences and vocalized instantly.</p>
            </div>
            <div className="step-number">03</div>
          </div>
        </div>
      </div>

    </div>
  );
}
