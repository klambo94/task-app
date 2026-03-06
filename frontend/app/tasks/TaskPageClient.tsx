"use client"

import {STATUS_FILTERS, Task, TaskCreate, TaskStatus} from "@/app/lib/types";
import {colors} from '@/app/lib/tokens'
import {Plus, Trash2} from "lucide-react"
import {useState} from 'react'
import {createTask, deleteTask, getTasks} from "@/app/lib/api";
import {TaskCard} from "@/app/components";


export default function TaskPageClient({initTasks}: { initTasks: Task[]}) {
    const[showCreateModal, setShowCreateModal] = useState(false)
    const[statusFilter, setStatusFilter] = useState<TaskStatus | string>("all")
    const[selectedIds, setSelectedIds] = useState<Set<number>>(new Set())
    const [newTask, setNewTask] = useState<TaskCreate>({ name: "", description: "", status: "open" })
    const [tasks, setTasks] = useState<Task[]>(initTasks)

    // when filter changes, refetch
    async function handleFilterChange(status: TaskStatus | undefined) {
        if ( typeof status == undefined) {
            setStatusFilter("all")
        } else {
            setStatusFilter(status as TaskStatus)

        }
        const data = await getTasks(status)
        setTasks(data)
    }

     async function refresh() {
        const data = await getTasks()
        setTasks(data)
        setStatusFilter("all")
    }

    async function handleDelete() {
        await Promise.all(Array.from(selectedIds).map((id) => deleteTask(id)))
        setSelectedIds(new Set())
        await refresh()
    }

    async function handleCreate() {
        if (!newTask.name.trim()) return
        await createTask(newTask)
        setNewTask({ name: "", description: "", status: "open" })
        setShowCreateModal(false)
        await refresh()
    }

    function toggleSelect(id: number | undefined) {
        setSelectedIds((prev) => {
            const next = new Set(prev)
            if (typeof id != undefined) {
                if (!next.has(id as number)) {
                    next.add(id as number)

                } else {
                    next.delete(id as number)
                }
            }
            return next
        })
    }


    return (
        <div className="grid grid-cols-[380px_1fr] min-h-screen  tracking-wide">
            {/* Left Sidebar */}
            <aside className="p-14">
                {/* Logo / Title */}
                <div>
                    <h1 className="flex-col text-5xl text-blue-black font-extrabold">Task <span className="flex-col text-light-purple">Board</span>
                    </h1>
                    <p className="text-3xl text-blue-gray font-semibold ">
                        {tasks.length} task{tasks.length !== 1 ? "s" : ""}
                    </p>
                </div>


                {/* Actions */}
                <div className="flex flex-col gap-3 pt-20">
                    <p className="text-3xl font-semibold text-blue-black">
                        Actions
                    </p>
                    <button className="btn btn-primary"
                            onClick={() => setShowCreateModal(true)}>
                        <Plus size={14}/> New Task
                    </button>
                    <button className="btn btn-danger"
                            onClick={handleDelete}
                            disabled={selectedIds.size === 0}>
                        <Trash2 size={14}/> Delete {selectedIds.size > 0 ? `(${selectedIds.size})` : ""}
                    </button>
                </div>


                {/* Filters - Status */}
                <div className="flex flex-col gap-3 pt-20">
                    <p className="text-3xl font-semibold text-blue-black">
                        Filter by Status
                    </p>

                    {STATUS_FILTERS.map((filter) =>(
                        <button
                            key={filter.value}
                            className="btn-filter"
                            onClick={() => setStatusFilter(filter.value)}
                            style={{
                                borderColor: statusFilter === filter.value ? filter.color : "transparent",
                                color: statusFilter === filter.value ? filter.color : colors.white,
                                background: colors.blueBlack,
                            }}
                        >
                            <span style={{
                                display: "inline-block",
                                width: "7px", height: "7px",
                                borderRadius: "50%",
                                backgroundColor: filter.color,
                                marginRight: "8px",
                            }} />
                            {filter.label}
                        </button>
                    ))}

                </div>

            </aside>

            {/* Main area */}
            <main className="pt-54">
                <div className="max-w-2xl">
                    {!showCreateModal &&
                        <div>
                            <h2 className="font-bold text-3xl text-blue-black mb-4">
                                {STATUS_FILTERS.find(filter => filter.value === statusFilter)?.label ?? "All"} Tasks
                            </h2>

                            {tasks.length === 0 ? (
                                <div style={{
                                    textAlign: "center",
                                    color: colors.blueGray,
                                    fontSize: "14px",
                                    fontStyle: "italic",
                                }}>
                                    No tasks found.
                                </div>
                            ) : (
                                tasks.map((task) => (
                                    <TaskCard
                                        key={task.id}
                                        task={task}
                                        onUpdated={refresh}
                                        onDeleted={refresh}
                                        selectedIds={selectedIds}
                                        onSelect={(id) => toggleSelect(id)}
                                    />
                                ))
                            )}
                        </div>
                    }

                    {/*  Create Modal  */}
                    {showCreateModal && (
                        <div className="modal-overlay align-middle"
                             onClick={() => setShowCreateModal(!showCreateModal)}>
                            <div className="modal" onClick={(e) => e.stopPropagation()}>
                                <h3 className="">
                                    New Task
                                </h3>

                                <div className="">
                                    <div>
                                        <label>Title</label>
                                        <input placeholder="Task Name"
                                               value={newTask.name}
                                               onChange={(e) => setNewTask({ ...newTask, name: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <label>Description</label>
                                        <textarea placeholder="Optional Description..."
                                                  value={newTask.description ?? ""}
                                                  onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <label>Status</label>
                                        <select
                                            value={newTask.status}
                                            onChange={(e) => setNewTask({ ...newTask, status: e.target.value as TaskCreate["status"] })}
                                        >
                                            <option value={TaskStatus.OPEN}>Open</option>
                                            <option value={TaskStatus.IN_PROGRESS}>In Progress</option>
                                            <option value={TaskStatus.COMPLETED}>Completed</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="flex gap-10 mt-24 justify-end ml-auto" >
                                    <button className="btn border-2 border-red-300 max-w-1/4  text-red  ml-auto hover:bg-red-300" onClick={() => setShowCreateModal(false)}>
                                        Cancel
                                    </button>
                                    <button className="btn btn-primary" onClick={handleCreate} disabled={!newTask.name.trim()}>
                                        Create Task
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>


            </main>


        </div>


    )
}