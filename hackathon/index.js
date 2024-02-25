const videoElement = document.getElementById('videoElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const playButton = document.getElementById('playButton');
const submitButton = document.getElementById('submitButton');

let mediaRecorder;
let recordedChunks = [];

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);
playButton.addEventListener('click', playRecording);
submitButton.addEventListener('click', submitRecording);

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    videoElement.srcObject = stream;
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();
    
    startButton.disabled = true;
    stopButton.disabled = false;
}

function stopRecording() {
    mediaRecorder.stop();
    videoElement.srcObject.getTracks().forEach(track => track.stop());
    startButton.disabled = false;
    stopButton.disabled = true;
    playButton.disabled = false;
    submitButton.disabled = false;
}

function playRecording() {
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    const url = URL.createObjectURL(blob);
    const video = document.createElement('video');
    video.controls = true;
    video.src = url;
    videoElement.replaceWith(video);
}

function submitRecording() {
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    const formData = new FormData();
    formData.append('video', blob, 'recording.webm');
    
    // Submit formData using fetch or XMLHttpRequest
    // Example using fetch:
    /*
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // Handle response
    })
    .catch(error => {
        console.error('Error:', error);
    });
    */
}

function handleDataAvailable(event) {
    if (event.data.size > 0) {
        recordedChunks.push(event.data);
    }
}