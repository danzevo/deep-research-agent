<script setup lang="ts">
// Accept the tasks array from the parent
defineProps<{
    tasks: any[]
}>()
</script>
<template>
    <div>
        <h2 class="text-2xl font-bold mb-6 text-slate-200">Recent tasks</h2>
        <div class="space-y-4">
            <div v-for="task in tasks.slice().reverse()" :key="task.id"
                class="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:border-indigo-500/50 transition-colors">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-xl font-semibold text-white">{{ task.topic }}</h3>
                    <span v-if="task.status === 'PENDING'" class="px-3 py-1 bg-yellow-500/10 text-yellow-400 rounded-full text-sm font-medium border border-yellow-500/20">
                        Pending in RabbitMQ...
                    </span>
                    <span v-else-if="task.status === 'COMPLETED'" class="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-sm font-medium border border-emerald-500/20">
                        Completed
                    </span>
                </div>
                <div v-if="task.resultMarkdown" class="bg-slate-950 p-4 rounded-lg text-slate-300 text-sm overflow-y-auto max-h-64 whitespace-pre-wrap font-mono">
                    {{ task.resultMarkdown }}
                </div>
            </div>
        </div>
    </div>
</template>