<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TaskForm from './components/TaskForm.vue'
import TaskList from './components/TaskList.vue'
import { fetchAllTasks } from './api'

const tasks = ref<any[]>([])

const fetchTasks = async () => {
  try {    
    tasks.value = await fetchAllTasks()
  } catch (error) {
    console.error("Error fetching tasks:", error)
  }
}

// Fetch tasks when page loads
onMounted(fetchTasks)
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 font-sans p-8 selection:bg-indigo-500/30">
    <header class="max-w-5xl mx-auto mb-12 text-center space-y-4">
      <h1 class="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
        Enterprise AI Researcher
      </h1>
      <p class="text-slate-400 text-lg max-w-2xl mx-auto">
        Event-driven Microservice Architecture powering deep, autonomous web research.
      </p>
    </header>
    <main class="max-w-3xl mx-auto">
      <!-- 1. The Input Component (Listens for 'task-submitted' event) -->
      <TaskForm @task-submitted="fetchTasks"/>
      <!-- 2. The List Component (Passes the 'tasks' state down) -->
      <TaskList :tasks="tasks" />
    </main>
  </div>
</template>
