const videoElement = document.getElementById('videoElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const playButton = document.getElementById('playButton');
const submitButton = document.getElementById('submitButton');

let mediaRecorder;
let recordedChunks = [];
let audioBlob;

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);
playButton.addEventListener('click', playRecording);
submitButton.addEventListener('click', submitRecording);

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    videoElement.srcObject = stream;
    
    // Only record audio
    const audioStream = new MediaStream(stream.getAudioTracks());
    mediaRecorder = new MediaRecorder(audioStream);

    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();

    mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: 'audio/mp3' });
        audioBlob = blob;
        const url = URL.createObjectURL(blob);
        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = url;
        videoElement.replaceWith(audio);
    };
    
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
    const url = URL.createObjectURL(audioBlob);
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.src = url;
    videoElement.replaceWith(audio);
}

async function submitRecording() {
    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.mp3');

        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        })
        const json = await response.json()
        document.querySelector('pre').innerHTML = JSON.parse(json.suggestions).choices[0].message.content
    } catch (err) {
        console.error(err)
    }
}

function handleDataAvailable(event) {
    if (event.data.size > 0) {
        recordedChunks.push(event.data);
    }
}
