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
//function to reset the stats
function resetStats() {
    fetch('/reset_stats', {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to reset stats');
        return response.json();
    })
    .then(data => {
        updateStats(); // After reset, update the UI
    })
    .catch(error => {
        feedbackSpan.innerText = 'Failed to reset stats';
        console.error('Error resetting stats:', error);
    });
}

function startExercise() {
    fetch('/start_exercise', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.message));
}

function stopExercise() {
    fetch('/stop_exercise', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.message));
}

// Refresh stats button
refreshButton.addEventListener('click', resetStats);

// Auto update stats every second
setInterval(updateStats, 1000);
