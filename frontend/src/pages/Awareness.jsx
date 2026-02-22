import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Awareness() {
    const [patterns, setPatterns] = useState([]);

    useEffect(() => {
        // Fetch patterns from backend if available, else show defaults
        axios.get('http://localhost:5000/api/scam-patterns')
            .then(res => setPatterns(res.data))
            .catch(() => {
                // Fallback
                setPatterns([
                    { pattern: "Registration Fees", description: "Legitimate companies never ask for money to hire you." },
                    { pattern: "Unprofessional Emails", description: "Offers from @gmail.com or @yahoo.com instead of company domains." },
                    { pattern: "Immediate Joining", description: "Pressure to join immediately without proper interviews." }
                ]);
            });
    }, []);

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <h1>Safety & Awareness</h1>
                <p className="subtitle">Common indicators of fake job offers in India.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>

                {/* Static Tips Card */}
                <div className="glass-panel" style={{ padding: '1.5rem', gridColumn: '1 / -1' }}>
                    <h2 style={{ color: '#34d399' }}>✅ Best Practices</h2>
                    <ul style={{ paddingLeft: '1.5rem', lineHeight: '1.6', color: '#e2e8f0' }}>
                        <li>Always verify the company on LinkedIn and Google.</li>
                        <li>Check the career page of the official company website.</li>
                        <li>Never pay for laptops, uniforms, or training kits before joining.</li>
                        <li>Avoid sharing OTPs or bank passwords during 'interviews'.</li>
                    </ul>
                </div>

                {/* Dynamic Patterns */}
                {patterns.map((p, i) => (
                    <div key={i} className="glass-panel" style={{ padding: '1.5rem', borderLeft: '4px solid #f59e0b' }}>
                        <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>⚠️ {p.pattern}</h3>
                        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>{p.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Awareness;
