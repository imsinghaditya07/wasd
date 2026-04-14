import React from 'react';
import { History as HistoryIcon, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function History() {
  const historyData = [
    { time: '10 mins ago', type: 'Sign → Speech', value: 'Hello' },
    { time: '1 hour ago', type: 'Speech → Sign', value: 'Thank you' },
    { time: 'Yesterday', type: 'Sign → Speech', value: 'Please help' }
  ];

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out', padding: '40px 0' }}>
      <div style={{ marginBottom: '32px' }}>
        <Link to="/dashboard" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', color: 'var(--primary-accent)', textDecoration: 'none', marginBottom: '16px' }}>
          <ArrowLeft size={18} /> Back to Dashboard
        </Link>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <HistoryIcon size={32} color="var(--primary-accent)" /> 
          Translation History
        </h1>
        <p style={{ color: 'var(--text-muted)' }}>A log of your recent translated signs and speech.</p>
      </div>

      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {historyData.map((item, idx) => (
          <div key={idx} style={{ padding: '16px', borderBottom: idx !== historyData.length - 1 ? '1px solid var(--glass-border)' : 'none', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '4px' }}>{item.time} ({item.type})</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 500 }}>{item.value}</div>
            </div>
          </div>
        ))}
        {historyData.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '32px 0' }}>
            No history found. Try translating something!
          </div>
        )}
      </div>
    </div>
  );
}
