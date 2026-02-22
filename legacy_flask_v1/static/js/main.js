document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const jobInput = document.getElementById('job-input');
    const resultContainer = document.getElementById('result-container');
    const btnText = document.getElementById('btn-text');
    const spinner = document.getElementById('loading-spinner');
    
    // Result Elements
    const resultTitle = document.getElementById('result-title');
    const resultBadge = document.getElementById('result-badge');
    const predictionText = document.getElementById('prediction-text');
    const flagsList = document.getElementById('flags-list');
    const circlePath = document.querySelector('.circle');
    const percentageText = document.querySelector('.percentage');

    analyzeBtn.addEventListener('click', async () => {
        const text = jobInput.value.trim();
        if (!text) {
            alert("Please paste a job offer text.");
            return;
        }

        // UI Loading State
        setLoading(true);
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            displayResult(data);

        } catch (error) {
            console.error(error);
            alert("An error occurred while analyzing.");
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
            analyzeBtn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    }

    function displayResult(data) {
        resultContainer.classList.remove('hidden');

        // Update Badge and Color
        const isFake = data.overall_status === 'Fake';
        resultBadge.textContent = data.overall_status;
        resultBadge.className = `badge ${isFake ? 'fake' : 'safe'}`;

        // Update Prediction Text
        predictionText.innerHTML = `Prediction: <strong>${data.overall_status}</strong>`;

        // Update Confidence Circle
        const confidence = Math.round(data.confidence);
        const strokeColor = isFake ? '#ef4444' : '#22c55e'; // Red or Green
        
        percentageText.textContent = `${confidence}%`;
        circlePath.style.stroke = strokeColor;
        
        // Reset animation to trigger it again
        circlePath.style.strokeDasharray = `0, 100`;
        setTimeout(() => {
            circlePath.style.strokeDasharray = `${confidence}, 100`;
        }, 100);

        // Update Flags
        flagsList.innerHTML = '';
        if (data.flags && data.flags.length > 0) {
            data.flags.forEach(flag => {
                const li = document.createElement('li');
                li.textContent = flag;
                flagsList.appendChild(li);
            });
        } else if (isFake) {
             const li = document.createElement('li');
             li.textContent = "AI Model detected suspicious patterns.";
             flagsList.appendChild(li);
        } else {
             const li = document.createElement('li');
             li.textContent = "No obvious scam patterns found.";
             li.style.background = 'rgba(34, 197, 94, 0.1)';
             li.style.color = '#86efac';
             li.style.borderLeftColor = '#22c55e';
             flagsList.appendChild(li);
        }
    }
});
