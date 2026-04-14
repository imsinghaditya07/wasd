import React from 'react';
import { Shield, Target, Cpu, Users, Heart, Zap, Globe, MessageSquare } from 'lucide-react';

export default function About() {
  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', animation: 'fadeIn 0.7s ease-out', padding: '60px 0' }}>
      
      {/* HEADER */}
      <div style={{ textAlign: 'center', marginBottom: '80px' }}>
         <div style={{ display: 'inline-flex', padding: '8px 16px', background: 'rgba(6, 182, 212, 0.1)', borderRadius: '100px', color: 'var(--primary-accent)', fontSize: '0.75rem', fontWeight: 800, marginBottom: 24, letterSpacing: '0.1em', textTransform: 'uppercase', border: '1px solid rgba(6, 182, 212, 0.2)' }}>
            The Story Behind the AI
         </div>
         <h1 style={{ fontSize: '3.5rem', marginBottom: '20px', letterSpacing: '-0.04em' }}>
            Bridging Beyond <span className="text-gradient">Silence</span>
         </h1>
         <p style={{ color: 'var(--text-muted)', fontSize: '1.25rem', maxWidth: '700px', margin: '0 auto' }}>
            We are redefining how millions of deaf and hard-of-hearing individuals interact with the world around them.
         </p>
      </div>

      {/* CORE SECTIONS */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', marginBottom: '80px' }}>
         <div className="card" style={{ padding: '40px' }}>
            <div style={{ color: '#ef4444', marginBottom: 20 }}><Target size={40} /></div>
            <h2 style={{ fontSize: '1.75rem', marginBottom: 20 }}>The Challenge</h2>
            <p style={{ lineHeight: 1.7, color: 'var(--text-muted)' }}>
              Over <b>70 million</b> people worldwide use sign language as their primary communication. Despite this, they face massive barriers in healthcare, banking, and public spaces where interpreters aren't available. In India alone, there are <b>63 million</b> people with hearing impairments who lack basic assistive communication tools.
            </p>
         </div>
         <div className="card" style={{ padding: '40px' }}>
            <div style={{ color: 'var(--primary-accent)', marginBottom: 20 }}><Heart size={40} /></div>
            <h2 style={{ fontSize: '1.75rem', marginBottom: 20 }}>The Mission</h2>
            <p style={{ lineHeight: 1.7, color: 'var(--text-muted)' }}>
              SilentBridge was born from a simple idea: <b>Communication is a human right.</b> Our goal is to provide a zero-cost, high-performance, and privacy-focused digital interpreter that resides in your pocket, turning any phone or laptop into a bridge between silence and sound.
            </p>
         </div>
      </div>

      {/* TECH STACK */}
      <div style={{ marginBottom: '100px' }}>
         <h2 style={{ fontSize: '2rem', marginBottom: '40px', textAlign: 'center' }}>Our Technical Core</h2>
         <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
            <div className="card" style={{ padding: '32px', textAlign: 'center' }}>
                <div style={{ width: 64, height: 64, borderRadius: 16, background: 'rgba(255,255,255,0.02)', margin: '0 auto 24px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--secondary-accent)' }}>
                    <Cpu size={32} />
                </div>
                <h4 style={{ marginBottom: 12 }}>Edge Inference</h4>
                <p style={{ fontSize: '0.9rem' }}>Real-time LSTM processing on your local hardware for 0ms latency.</p>
            </div>
            <div className="card" style={{ padding: '32px', textAlign: 'center' }}>
                <div style={{ width: 64, height: 64, borderRadius: 16, background: 'rgba(255,255,255,0.02)', margin: '0 auto 24px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#10b981' }}>
                    <Shield size={32} />
                </div>
                <h4 style={{ marginBottom: 12 }}>Privacy First</h4>
                <p style={{ fontSize: '0.9rem' }}>Frames are processed locally. No video data ever leaves your device.</p>
            </div>
            <div className="card" style={{ padding: '32px', textAlign: 'center' }}>
                <div style={{ width: 64, height: 64, borderRadius: 16, background: 'rgba(255,255,255,0.02)', margin: '0 auto 24px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#f59e0b' }}>
                    <Globe size={32} />
                </div>
                <h4 style={{ marginBottom: 12 }}>Inclusive Design</h4>
                <p style={{ fontSize: '0.9rem' }}>Built with WCAG AAA accessibility standards from the ground up.</p>
            </div>
         </div>
      </div>

      {/* FINAL CTA */}
      <div className="card" style={{ padding: '60px', textAlign: 'center', border: '1px dashed var(--primary-accent)', background: 'linear-gradient(rgba(6, 182, 212, 0.05), transparent)' }}>
         <h2 style={{ fontSize: '2rem', marginBottom: '16px' }}>Ready to start communicating?</h2>
         <p style={{ marginBottom: '32px', color: 'var(--text-muted)' }}>Join us in creating a world where no voice goes unheard.</p>
         <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
            <button className="btn btn-primary shadow-glow">Start Interpreting Now</button>
            <button className="btn btn-outline" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <MessageSquare size={18} /> Contact Team
            </button>
         </div>
      </div>

    </div>
  );
}
