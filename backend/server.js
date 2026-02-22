require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const axios = require('axios');

// Import Models
const JobReport = require('./models/JobReport');
const ScamPattern = require('./models/ScamPattern');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/jobcheq';
mongoose.connect(MONGO_URI)
    .then(async () => {
        console.log('MongoDB Connected');
        // Seed patterns if empty
        const count = await ScamPattern.countDocuments();
        if (count === 0) {
            await ScamPattern.insertMany([
                { pattern: "Registration Fee", description: "Asking for money before hiring", severity: "High" },
                { pattern: "No Interview", description: "Direct offer without screening", severity: "High" },
                { pattern: "Whatsapp Contact Only", description: "Communication only via chat apps", severity: "Medium" }
            ]);
            console.log('Seeded initial scam patterns');
        }
    })
    .catch(err => console.log('MongoDB Connection Error:', err.message));

// Routes

/*
 * POST /api/analyze-job
 * Input: jobDescription, recruiterEmail, companyName, jobURL
 * Output: verdict, confidenceScore, reasons[]
 */
app.post('/api/analyze-job', async (req, res) => {
    const { jobDescription, recruiterEmail, companyName, jobURL } = req.body;

    if (!jobDescription) {
        return res.status(400).json({ error: 'Job Description is required' });
    }

    try {
        // Construct prompt for ML service
        const combinedText = `
            Company: ${companyName || 'Unknown'}
            Email: ${recruiterEmail || 'Unknown'}
            Job Description: ${jobDescription}
        `.trim();

        // Call Python Microservice
        // Note: Ensure Python service is running on PORT 5001
        let mlResponse;
        try {
            mlResponse = await axios.post('http://localhost:5001/predict', { text: combinedText });
        } catch (connErr) {
            console.error("ML Service unreachable:", connErr.message);
            // Fallback mock response if ML is down (for development stability)
            mlResponse = { data: { verdict: 'Fake', confidence: 0, flags: ['ML Service Unavailable'] } };
        }

        const { verdict: mlVerdict, confidence, flags } = mlResponse.data;

        // Logic to determine Final Verdict (Genuine | Suspicious | Fake)
        let finalVerdict = 'Genuine';
        let finalReasons = flags || [];

        // Add heuristics
        if (recruiterEmail && recruiterEmail.endsWith('@gmail.com')) {
            finalReasons.push('Unprofessional Email Domain (@gmail.com)');
        }

        if (finalReasons.length > 0 || mlVerdict === 'Fake') {
            if (confidence > 80 || finalReasons.length >= 2) {
                finalVerdict = 'Fake';
            } else {
                finalVerdict = 'Suspicious';
            }
        }

        const result = {
            verdict: finalVerdict,
            confidenceScore: confidence,
            reasons: finalReasons,
            timestamp: new Date()
        };

        // Save Analysis Log (Optional, but good for reporting later)
        // const report = new JobReport({ ...req.body, ...result });
        // await report.save();

        res.json(result);

    } catch (error) {
        console.error("Error in /api/analyze-job:", error.message);
        res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
});

/*
 * POST /api/report-scam
 * Input: Analysis result + user confirmation
 */
app.post('/api/report-scam', async (req, res) => {
    try {
        const reportData = req.body;
        const newReport = new JobReport(reportData);
        await newReport.save();
        res.status(201).json({ message: 'Report saved successfully', reportId: newReport._id });
    } catch (error) {
        console.error("Error saving report:", error.message);
        res.status(500).json({ error: 'Failed to save report' });
    }
});

/*
 * GET /api/scam-patterns
 * Return common scam indicators
 */
app.get('/api/scam-patterns', async (req, res) => {
    try {
        const patterns = await ScamPattern.find();
        res.json(patterns);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch patterns' });
    }
});

// Backward compatibility (optional, for existing frontend if not updated immediately)
app.post('/api/analyze', async (req, res) => {
    res.redirect(307, '/api/analyze-job'); // 307 preserves POST method/body
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Node Server running on port ${PORT}`);
});
