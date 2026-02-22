const mongoose = require('mongoose');

const JobReportSchema = new mongoose.Schema({
    jobDescription: { type: String, required: true },
    recruiterEmail: { type: String },
    companyName: { type: String },
    jobURL: { type: String },
    verdict: { type: String, enum: ['Genuine', 'Suspicious', 'Fake'], required: true },
    confidenceScore: { type: Number },
    scamReasons: [{ type: String }],
    reportedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('JobReport', JobReportSchema);
