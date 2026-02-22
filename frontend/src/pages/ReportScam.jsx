import React, { useState } from 'react';
import axios from 'axios';

function ReportScam() {
    const [formData, setFormData] = useState({
        companyName: '',
        jobDescription: '',
        scamType: 'Registration Fee',
        reporterNote: ''
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            // We reuse the basic report endpoint, adapting data
            await axios.post('http://localhost:5000/api/report-scam', {
                ...formData,
                verdict: 'Fake', // User is reporting it as fake
                confidenceScore: 100,
                scamReasons: [formData.scamType, formData.reporterNote]
            });
            alert('Thank you! Your report has been added to our database.');
            setFormData({ companyName: '', jobDescription: '', scamType: 'Registration Fee', reporterNote: '' });
        } catch (err) {
            alert('Failed to submit report. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <h1>Report a Scam</h1>
                <p className="subtitle">Help others by reporting fraudulent job offers.</p>
            </header>

            <div className="glass-panel" style={{ padding: '2rem' }}>
                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1rem' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Company/Recruiter Name</label>
                        <input
                            type="text"
                            className="input-field"
                            required
                            value={formData.companyName}
                            onChange={e => setFormData({ ...formData, companyName: e.target.value })}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Type of Scam</label>
                        <select
                            className="input-field"
                            value={formData.scamType}
                            onChange={e => setFormData({ ...formData, scamType: e.target.value })}
                            style={{ width: '100%', background: 'rgba(15, 23, 42, 0.6)' }}
                        >
                            <option>Registration Fee / Money Request</option>
                            <option>Fake Offer Letter</option>
                            <option>Data Theft / Phishing</option>
                            <option>Unprofessional Behavior</option>
                            <option>Other</option>
                        </select>
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Job Details / Evidence</label>
                        <textarea
                            className="input-field"
                            style={{ height: '100px' }}
                            required
                            value={formData.jobDescription}
                            onChange={e => setFormData({ ...formData, jobDescription: e.target.value })}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Additional Notes</label>
                        <textarea
                            className="input-field"
                            style={{ height: '80px' }}
                            value={formData.reporterNote}
                            onChange={e => setFormData({ ...formData, reporterNote: e.target.value })}
                        />
                    </div>

                    <button type="submit" className="btn-primary" disabled={loading}>
                        {loading ? 'Submitting...' : 'Submit Report'}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ReportScam;
