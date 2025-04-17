const exerciseSelect = document.getElementById('exercise');
const repCountSpan = document.getElementById('repCount');
const caloriesBurnedSpan = document.getElementById('caloriesBurned');
const feedbackSpan = document.getElementById('feedback');
const refreshButton = document.getElementById('refreshStats');

// Handle exercise selection change
exerciseSelect.addEventListener('change', function () {
    fetch('/set_exercise', {
        method: 'POST',
        body: JSON.stringify({ exercise: this.value }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to set exercise');
        feedbackSpan.innerText = 'Exercise updated successfully!';
    })
    .catch(error => {
        feedbackSpan.innerText = 'Failed to update exercise';
        console.error('Error setting exercise:', error);
    });
});

// Function to update stats
function updateStats() {
    fetch('/get_stats')
    .then(response => {
        if (!response.ok) throw new Error('Failed to fetch stats');
        return response.json();
    })
    .then(data => {
        repCountSpan.innerText = data.reps;
        caloriesBurnedSpan.innerText = data.calories.toFixed(2);
        feedbackSpan.innerText = data.feedback;
    })
    .catch(error => {
        feedbackSpan.innerText = 'Failed to update stats';
        console.error('Error updating stats:', error);
    });
}

// Refresh stats button
refreshButton.addEventListener('click', updateStats);

// Auto update stats every second
setInterval(updateStats, 1000);
