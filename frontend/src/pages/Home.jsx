import React, { useState } from 'react';
import axios from 'axios';

function Home() {
    const [formData, setFormData] = useState({
        jobDescription: '',
        companyName: '',
        recruiterEmail: '',
        jobURL: ''
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleAnalyze = async () => {
        if (!formData.jobDescription.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await axios.post('http://localhost:5000/api/analyze-job', formData);
            setResult(response.data);
        } catch (err) {
            console.error(err);
            setError('Failed to analyze. Ensure backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const getVerdictClass = (verdict) => {
        if (verdict === 'Fake') return 'verdict-fake';
        if (verdict === 'Suspicious') return 'verdict-suspicious';
        return 'verdict-real';
    };

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <h1>Detect Fake Jobs</h1>
                <p className="subtitle">Paste job details below to verify authenticity artificially.</p>
            </header>

            <div className="glass-panel" style={{ padding: '2rem' }}>
                <div style={{ display: 'grid', gap: '1rem', marginBottom: '1rem' }}>
                    <input
                        type="text"
                        name="companyName"
                        placeholder="Company Name (Optional)"
                        className="input-field"
                        value={formData.companyName}
                        onChange={handleChange}
                    />
                    <input
                        type="email"
                        name="recruiterEmail"
                        placeholder="Recruiter Email (Optional)"
                        className="input-field"
                        value={formData.recruiterEmail}
                        onChange={handleChange}
                    />
                    <input
                        type="url"
                        name="jobURL"
                        placeholder="Job Posting URL (Optional)"
                        className="input-field"
                        value={formData.jobURL}
                        onChange={handleChange}
                    />
                </div>

                <textarea
                    name="jobDescription"
                    placeholder="Paste the job description, email, or message here..."
                    value={formData.jobDescription}
                    onChange={handleChange}
                />
                <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                    <button
                        className="btn-primary"
                        onClick={handleAnalyze}
                        disabled={loading || !formData.jobDescription}
                    >
                        {loading ? <div className="loader"></div> : 'ANALYZE NOW'}
                    </button>
                </div>
            </div>

            {error && (
                <div className="glass-panel" style={{ padding: '1rem', color: '#ef4444', textAlign: 'center', marginTop: '1rem' }}>
                    {error}
                </div>
            )}

            {result && (
                <div className="glass-panel result-card">
                    <div className={`verdict-badge ${getVerdictClass(result.verdict)}`}>
                        {result.verdict}
                    </div>

                    <div className="confidence-meter">
                        <span>Confidence Score</span>
                        <span className="confidence-value">{result.confidenceScore}%</span>
                    </div>

                    {result.reasons && result.reasons.length > 0 && (
                        <div className="flags-list">
                            <h3>⚠️ Risk Factors:</h3>
                            {result.reasons.map((flag, index) => (
                                <div key={index} className="flag-item">
                                    • {flag}
                                </div>
                            ))}
                        </div>
                    )}

                    {result.verification_logs && result.verification_logs.length > 0 && (
                        <div className="flags-list" style={{ marginTop: '1rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                            <h3 style={{ color: '#60a5fa' }}>🌐 Network Verification:</h3>
                            {result.verification_logs.map((log, index) => (
                                <div key={index} className="flag-item" style={{ color: '#93c5fd' }}>
                                    • {log}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Home;
