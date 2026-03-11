"use client"

import {STATUS_FILTERS, Task, TaskCreate, TaskStatus, TaskUpdate} from "@/app/lib/types";
import {colors} from '@/app/lib/tokens'
import {Plus, Trash2} from "lucide-react"
import {useState, useCallback} from 'react'
import {createTask, deleteTask, getTasks, updateTask} from "@/app/lib/api";
import TaskCard from "@/app/task/TaskCard";


export default function TaskPageClient({initTasks}: { initTasks: Task[]}) {
    const[showCreateModal, setShowCreateModal] = useState(false)
    const [editingTask, setEditingTask] = useState<Task | null>(null)
    const[statusFilter, setStatusFilter] = useState<TaskStatus | undefined>(undefined)
    const[selectedIds, setSelectedIds] = useState<Set<number>>(new Set())
    const [newTask, setNewTask] = useState<TaskCreate>({ name: "", description: "", status: "open" })
    const [tasks, setTasks] = useState<Task[]>(initTasks)


    const refresh = useCallback(async (status?: TaskStatus) => {
        const data = await getTasks(status)
        setTasks(data)
        setStatusFilter(status)
    }, [])


    const openCreate = () => {
        setEditingTask(null)
        setShowCreateModal(true)
    }

    const openEdit = (task: Task) => {
        setEditingTask(task)
        setShowCreateModal(true)
    }

    async function handleFilterChange(status: TaskStatus | undefined) {
        setStatusFilter(status)
        await refresh(status)  // pass it directly, don't rely on state
    }

    async function handleDelete(id:number | Set<number>) {
        if(id instanceof Set) {
            await Promise.all(Array.from(selectedIds).map((id) => deleteTask(id)))
            setSelectedIds(new Set())
        } else {
            await deleteTask(id as number)

        }
        await refresh()
    }

    async function handleUpdate(task: Task) {
        if (task != null && task.id != null) {
            try {
                const update: TaskUpdate = {
                    name: task.name,
                    description: task.description,
                    status: task.status
                }

                await updateTask(task.id, update)
                await refresh(task.status)
                console.debug("Status Updated")
            } catch (e) {
                // console.error("ERROR - Unable to update status")
                console.error(e)
            }
        } else {
            throw Error("Please select a task to update")
        }
    }


    async function handleSave() {
        if (editingTask) {
            await updateTask(editingTask.id, {
                name: editingTask.name,
                description: editingTask.description,
                status: editingTask.status
            })
            setStatusFilter(editingTask.status)
        } else {
            // create mode
            await createTask(newTask)
            setStatusFilter(undefined)
        }
        setShowCreateModal(false)
        setEditingTask(null)
        setNewTask({ name: "", description: "", status: TaskStatus.OPEN })
        refresh(statusFilter)
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
                            onClick={event => handleDelete(selectedIds)}
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
                            key={filter.label}
                            className="btn-filter"
                            onClick={() => {handleFilterChange(filter.value)}}
                            style={{
                                borderColor: filter.color,
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
                                        onUpdated={(task:Task) => handleUpdate(task)}
                                        onDeleted={(id) => handleDelete(id)}
                                        onEdit={(task:Task) => openEdit(task)}
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
                                <h3>
                                     {editingTask ? "Edit Task" : "Create New Task"}
                                </h3>

                                <div className="flex flex-col gap-4">
                                    <div className="flex flex-col gap-1">
                                        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Title</label>
                                        <input
                                            className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                                            placeholder="Task Name"
                                            value={editingTask ? editingTask.name :newTask.name}
                                            onChange={(e) => {
                                                if(editingTask !=  null) {
                                                    setEditingTask({...editingTask, name: e.target.value})
                                                } else {
                                                    setNewTask({ ...newTask, name: e.target.value })
                                                }}
                                            }/>
                                    </div>
                                    <div className="flex flex-col gap-1">
                                        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Description</label>
                                        <textarea
                                            className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400 resize-none h-24"
                                            placeholder="Optional Description..."
                                            value={editingTask ? editingTask.description ?? "" : newTask.description ?? ""}
                                            onChange={(e) => {
                                                if(editingTask !=  null) {
                                                    setEditingTask({...editingTask, description: e.target.value})
                                                } else {
                                                    setNewTask({ ...newTask, description: e.target.value })
                                                }}}
                                        />
                                    </div>
                                    <div className="flex flex-col gap-1">
                                        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</label>
                                        <select
                                            className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                                            value={newTask.status}
                                            onChange={(e) =>{
                                                if(editingTask !=  null) {
                                                    setEditingTask({...editingTask, status: e.target.value as TaskCreate["status"]})
                                                } else {
                                                   setNewTask({ ...newTask, status: e.target.value as TaskCreate["status"] })}
                                                }}
                                        >
                                            <option value={TaskStatus.OPEN}>Open</option>
                                            <option value={TaskStatus.IN_PROGRESS}>In Progress</option>
                                            <option value={TaskStatus.COMPLETED}>Completed</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="flex gap-10 mt-24 justify-end ml-auto" >
                                    <button className="btn border-2 border-red-300 max-w-1/4  text-red  ml-auto hover:bg-red-300"
                                            onClick={() => {
                                                setShowCreateModal(false)
                                                setNewTask({name: "", description: "", status: TaskStatus.OPEN})
                                                setEditingTask(null)
                                            }}
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        className="btn btn-primary"
                                        onClick={handleSave}
                                        disabled={editingTask ? !editingTask.name?.trim() : !newTask.name?.trim()}
                                    >
                                        {editingTask ? "Save" : "Create Task"}
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