<template>
  <div class="mb-3 text-center">
    <button
      @click="recording ? stopRecording() : startRecording()"
      :class="['btn', 'btn-lg', 'w-100', recording ? 'neon-btn' : 'neon-btn']"
      :style="recording
        ? 'background: linear-gradient(90deg, #ff00cc 0%, #333399 100%); color: #fff; font-weight: bold; border-radius: 1rem; box-shadow: 0 0 16px #ff00cc;'
        : ''"
    >
      {{ recording ? 'Stop Recording' : 'Start Voice Diagnosis' }}
    </button>
    <div v-if="loading" class="mt-2" style="color: #00fff7; font-weight: bold;">
      <span class="spinner-border spinner-border-sm me-2" style="border-color: #00fff7;"></span>
      Analyzing...
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recording: false,
      mediaRecorder: null,
      audioChunks: [],
      loading: false,
    };
  },
  methods: {
    async startRecording() {
      this.recording = true;
      this.audioChunks = [];

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (e) => this.audioChunks.push(e.data);
        this.mediaRecorder.start();
      } catch (err) {
        alert('❌ Microphone access denied or not supported.');
        this.recording = false;
      }
    },

    async stopRecording() {
      this.recording = false;
      this.mediaRecorder.stop();

      this.mediaRecorder.onstop = async () => {
        const blob = new Blob(this.audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('file', blob, 'audio.webm');

        this.loading = true;
        try {
          const res = await fetch('http://localhost:8000/analyze-audio/', {
            method: 'POST',
            body: formData,
          });
          const data = await res.json();
          this.$emit('audio-diagnosed', {
            response: data.response,
            transcription: data.transcription,
          });
        } catch (err) {
          this.$emit('audio-diagnosed', {
            response: '❌ Error connecting to backend.',
            transcription: '',
          });
        } finally {
          this.loading = false;
        }
      };
    },
  },
};
</script>