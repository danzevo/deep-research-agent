<script setup lang="ts">
import { ref } from 'vue'
import { submitResearchTask } from '../api'

const newTopic = ref('')
const isLoading = ref(false)

// Define the event we will emit to the parent when a task is submitted
const emit = defineEmits(['task-submitted'])

const submitTask = async () => {
    if (!newTopic.value) return
    isLoading.value = true

    try{
        await submitResearchTask(newTopic.value)
        newTopic.value = ''
        emit('task-submitted') // Shout up to App.vue to refresh the list!
    } catch (error) {
        console.error("Error:", error)
    } finally {
        isLoading.value = false
    }
}
</script>
<template>
    <div class="bg-slate-900/50 backdrop-blur-xl border border-slate-800 p-6 rounded-2xl shadow-2xl mb-12">
        <form @submit.prevent="submitTask" class="flex gap-4">
            <input 
                v-model="newTopic"
                type="text"
                placeholder="What should the AI research today...?"
                class="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-lg"
                :disabled="isLoading"
            />
            <button 
                type="submit"
                class="bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                :disabled="isLoading"
                >
                <span v-if="isLoading" class="animate-spin">🌀</span>
                <span v-else>Research</span>
            </button>
        </form>
    </div>
</template>