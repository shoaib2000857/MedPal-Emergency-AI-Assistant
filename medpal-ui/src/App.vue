<template>
  <main class="d-flex align-items-center justify-content-center" style="min-height: 100vh;">
    <div class="glass-card shadow-lg p-4 w-100" style="max-width: 1100px;">
      <h1 class="display-5 mb-4 neon-text text-center">
        🩺 MedPal <small class="text-info">Offline Medical Assistant</small>
      </h1>

      <!-- Voice diagnosis -->
      <RecordButton @audio-diagnosed="handleAudioResult" />

      <!-- Big scrollable, markdown-rendered conversation area -->
      <div
        class="conversation-markdown mb-3 p-4"
        style="height: 480px; overflow-y: auto; background: rgba(0,255,255,0.08); border-radius: 1.5rem; color: #e0f7fa;"
        ref="conversation"
      >
        <div v-for="(msg, idx) in chatHistory" :key="idx" class="mb-4">
          <div class="fw-bold text-info mb-1">You:</div>
          <div class="mb-2" v-html="marked.parse(msg.user)"></div>
          <div v-if="msg.transcript" class="text-secondary small mb-1">[Transcript: {{ msg.transcript }}]</div>
          <div class="fw-bold text-success mb-1">MedPal:</div>
          <div v-html="marked.parse(msg.assistant)" class="mb-2"></div>
        </div>
      </div>

      <!-- Input area -->
      <div class="d-flex flex-column flex-md-row gap-2">
        <textarea
          v-model="typedText"
          class="form-control mb-2 mb-md-0"
          rows="3"
          placeholder="Describe your symptoms here or ask a question..."
          style="flex: 1 1 auto;"
          @keyup.enter.exact.prevent="submitText"
        ></textarea>
        <button
          @click="submitText"
          :disabled="loading || !typedText"
          class="btn neon-btn"
          style="min-width: 160px; font-size: 1.2rem;"
        >
          {{ loading ? 'Analyzing...' : 'Send' }}
        </button>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import { marked } from 'marked';
import RecordButton from './components/RecordButton.vue';

export default {
  components: { RecordButton },
  data() {
    return {
      typedText: '',
      loading: false,
      chatHistory: [],
      marked,
    };
  },
  methods: {
    async submitText() {
      if (!this.typedText) return;
      const userMsg = this.typedText;
      this.loading = true;

      const historyForBackend = this.chatHistory.map(msg => ({
        user: msg.user,
        assistant: msg.assistant,
      }));

      try {
        const res = await axios.post('http://localhost:8000/analyze-text/', {
          text: userMsg,
          history: historyForBackend,
        });
        this.chatHistory.push({
          user: userMsg,
          assistant: res.data.response,
        });
        this.typedText = '';
        this.$nextTick(() => {
          const chatDiv = this.$refs.conversation;
          if (chatDiv) chatDiv.scrollTop = chatDiv.scrollHeight;
        });
      } catch (err) {
        this.chatHistory.push({
          user: userMsg,
          assistant: '❌ Error: Could not connect to backend.',
        });
      } finally {
        this.loading = false;
      }
    },
    handleAudioResult({ response, transcription }) {
      this.chatHistory.push({
        user: '[Voice Input]',
        assistant: response,
        transcript: transcription || '',
      });
      this.$nextTick(() => {
        const chatDiv = this.$refs.conversation;
        if (chatDiv) chatDiv.scrollTop = chatDiv.scrollHeight;
      });
    }
  },
};
</script>