const mongoose = require('mongoose');

const ScamPatternSchema = new mongoose.Schema({
    pattern: { type: String, required: true },
    description: { type: String },
    severity: { type: String, enum: ['High', 'Medium', 'Low'], default: 'Medium' },
    category: { type: String, default: 'General' }
});

module.exports = mongoose.model('ScamPattern', ScamPatternSchema);
