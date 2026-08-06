// Vite magically injects the .env variable using import.meta.env
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api'

// Centralized function to fetch tasks
export const fetchAllTasks = async () => {
    const response = await fetch(`${API_BASE_URL}/research`)
    return await response.json()
}

// Centralized function to submit tasks
export const submitResearchTask = async (topic: string) => {
    return await fetch(`${API_BASE_URL}/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
    })
}