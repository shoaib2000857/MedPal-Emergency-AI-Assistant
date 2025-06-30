<template>
  <div>
    <button @click="recording ? stopRecording() : startRecording()">
      {{ recording ? 'Stop Recording' : 'Start Voice Diagnosis' }}
    </button>

    <p v-if="loading">Analyzing...</p>
    <p v-if="result"><strong>Diagnosis:</strong> {{ result }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recording: false,
      mediaRecorder: null,
      audioChunks: [],
      result: '',
      loading: false
    };
  },
  methods: {
    async startRecording() {
      this.recording = true;
      this.audioChunks = [];

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = e => this.audioChunks.push(e.data);
        this.mediaRecorder.start();
      } catch (err) {
        alert('Microphone access denied or not supported.');
        this.recording = false;
      }
    },

    async stopRecording() {
      this.recording = false;
      this.mediaRecorder.stop();

      this.mediaRecorder.onstop = async () => {
        const blob = new Blob(this.audioChunks, { type: 'audio/webm' }); // safer than audio/wav
        const formData = new FormData();
        formData.append('file', blob, 'audio.webm');

        this.loading = true;
        try {
          const res = await fetch('http://localhost:8000/analyze-audio/', {
            method: 'POST',
            body: formData
          });
          const data = await res.json();
          this.result = data.result;
        } catch (err) {
          this.result = 'Error connecting to backend.';
        } finally {
          this.loading = false;
        }
      };
    }
  }
};
</script>
