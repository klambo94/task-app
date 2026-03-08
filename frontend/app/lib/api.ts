//all api calls to back end

import {TaskStatus, TaskUpdate, TaskCreate, Task} from "@/app/lib/types";


const API_URL = process.env.NEXT_PUBLIC_TASK_API

export async function getTasks(status?: TaskStatus): Promise<Task[]> {
    const url = status != undefined ? API_URL +`/tasks?status=${status}`
                            : API_URL + '/tasks'
    const res = await fetch(url)
    if(!res.ok) throw new Error("Failed to fetch tasks")
    return res.json()
}

export async function createTask(task: TaskCreate): Promise<Task> {
    const res = await fetch(API_URL +`/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task)
    })
    if (!res.ok) throw new Error("Failed to create task")
    return res.json()
}

export async function updateTask(id: number, task: TaskUpdate): Promise<Task> {
    const res = await fetch(API_URL +`/task/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(task)
    })
    if (!res.ok) throw new Error("Failed to update task")
    return res.json()
}

export async function deleteTask(id: number): Promise<void> {
    const res = await fetch(API_URL +`/task/${id}`, { method: "DELETE" })

    if (!res.ok) throw new Error("Failed to delete task")
}
