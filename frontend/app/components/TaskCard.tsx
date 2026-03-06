"use client"

import {useState} from "react"
import {updateTask, deleteTask} from "@/app/lib/api"
import {ChevronDown, Check, Trash2} from "lucide-react"
import {STATUS_FILTERS, Task, TaskStatus, TaskUpdate} from "@/app/lib/types";
import {colors} from "@/app/lib/tokens";


function formatDate(ts: string) {
    return new Date(ts).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    })
}

interface TaskCardProps {
    task: Task
    onUpdated: () => void
    onDeleted: () => void
    selectedIds: Set<number>
    onSelect: (id: number | undefined) => void

}

export default function TaskCard({task, onUpdated, onDeleted, selectedIds, onSelect }: TaskCardProps) {
    const[expanded, setExpanded] = useState(false)
    const[hovered, setHovered] = useState(false)
    const [showStatusMenu, setShowStatusMenu] = useState(false)
    const [currentStatus, setCurrentStatus] = useState(task.status)

    const isSelected = selectedIds.has(task.id)
    const isComplete = currentStatus === "completed"
    const currentStatusMeta = STATUS_FILTERS.find(f => f.value === currentStatus)

    async function handleStatusChange(newStatus: TaskStatus) {
        setShowStatusMenu(false)
        if (task.id != null) {
            try {
                const update: TaskUpdate = {
                    name: task.name,
                    description: task.description,
                    status: newStatus
                }

                await updateTask(task.id, update)
                setCurrentStatus(newStatus)
                console.debug("Status Updated")

            } catch (e) {
                // console.error("ERROR - Unable to update status")
                console.error(e)

            }
        } else {
            throw Error("Please select a task to update")
        }
    }


    async function handleDelete() {
        try {
            await deleteTask(task.id)
            onDeleted()
        } catch {
            console.error("Failed to delete task")
        }
    }

    return (
        <div className="pl-4 cursor-pointer rounded-lg border-1 border-solid py-5 mb-12 border-blue-black relative transition-shadow "
             style={{
                 boxShadow: expanded ? `0 8px 24px ${colors.lavender}25` : `0 1px 4px ${colors.white}`,
                 transform: expanded ? "translateY(-1px)" : "translateY(0)",}
             }
             onClick={() => onSelect(task.id)}
             onMouseEnter={() => setHovered(!hovered)}
             onMouseLeave={() => setHovered(!hovered)}>

            {/*  Display row  */}
            <div className="flex items-center">
                <div className="hover:bg-green-300 flex w-5 h-5 shrink rounded-sm transition-colors cursor-pointer "
                     style={{
                         border: isComplete ? "none" : `2px solid ${colors.blueBlack}`,
                         backgroundColor: isComplete ? "none" : "transparent",
                     }}
                     onClick={(e) => {
                         e.stopPropagation()  // prevent card click from also firing
                         const newStatus = isComplete ? TaskStatus.OPEN : TaskStatus.COMPLETED
                         handleStatusChange(newStatus)
                     }}
                >
                    {isComplete && <Check size={24} color={colors.green} strokeWidth={3} />}
                </div>
                <span className="flex pl-4"
                      style={{
                          textDecoration: isComplete ? "line-through" : "none",
                      }}
                >{task.name}</span>
                <div className="relative ml-auto">
                    <button className="btn btn-dropdown "
                            onClick={(e) =>{
                                e.stopPropagation()  // prevent card click from also firing
                                setShowStatusMenu(!showStatusMenu)}}>
                        {currentStatusMeta?.label}
                        <ChevronDown size={11} />
                    </button>

                    {/*Status Dropdown*/}
                    {showStatusMenu && (
                        <div className="absolute right-0 top-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10 min-w-36 overflow-hidden">
                            {STATUS_FILTERS.filter(f => f.value.toLowerCase() !== "all").map((filter) => (
                                <button
                                    key={filter.label}
                                    className="flex items-center gap-2 w-full px-3 py-2 text-xs text-left transition-colors whitespace-nowrap"
                                    style={{
                                        fontWeight: currentStatus === filter.value ? 600 : 400,
                                        color: currentStatus === filter.value ? filter.color : colors.blueGray,
                                        background: currentStatus === filter.value ? `${filter.color}18` : "transparent",
                                    }}
                                    onClick={(e) =>{
                                        e.stopPropagation()  // prevent card click from also firing
                                        handleStatusChange(filter.value as TaskStatus)}}
                                >
                                    <span style={{
                                        width: "7px",
                                        height: "7px",
                                        borderRadius: "50%",
                                        backgroundColor: filter.color,
                                        flexShrink: 0,
                                    }} />
                                    {filter.label}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
                {/* Chevron */}
                <ChevronDown
                    size={16}
                    onClick={(e) => {
                        e.stopPropagation()  // prevent card click from also firing
                        setExpanded(!expanded)}}
                    style={{
                        flexShrink: 0,
                        transform: expanded ? "rotate(180deg)" : "rotate(0deg)",
                        transition: "transform 0.25s ease",
                        color: colors.blueBlack,
                    }}
                />
                {/* Selected indicator bar */}
                {isSelected && (
                    <div className="absolute left-0 top-0 bottom-0 w-1 rounded-l-xl"
                         style={{ backgroundColor: colors.lightPurple }}
                    />
                )}

            </div>


            {/*  Expanded Content  */}
            <div className="pl-10 pt-5 pr-4" style={{
                overflow: "hidden",
                maxHeight: expanded ? "300px" : "0px",
                opacity: expanded ? 1 : 0,
                transition: "max-height 0.3s ease, opacity 0.25s ease",
            }}>
                <p className="margin-0 text-sm text-blue-black">
                    {task.description ?? "No description provided."}
                </p>

                <div className="flex items-center gap-4">
                     <span className="text-xs text-blue-black">
                        <span className="font-semibold text-blue-black">Created </span>
                         {formatDate(task.created_at)}
                    </span>
                    <span className="text-xs text-blue-black">
                        <span className="font-semibold text-blue-black">Updated </span>
                        {formatDate(task.updated_at)}
                    </span>

                    {/*  Delete Button  */}
                    <button className="btn border-2 border-red-300 max-w-1/4  text-red  ml-auto hover:bg-red-300"
                            onClick={(e) => { e.stopPropagation(); handleDelete() }}>
                        <Trash2 size={12} />
                        Delete
                    </button>
                </div>
            </div>
        </div>
    )}