"use client"

import {useState} from "react"
import {updateTask, deleteTask} from "@/app/lib/api"
import {ChevronDown, Check, Trash2, Pencil} from "lucide-react"
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
    onEdit: (task: Task) => void
    onUpdated: (task: Task) => void
    onDeleted: (id: number) => void
    selectedIds: Set<number>
    onSelect: (id: number | undefined) => void

}

export default function TaskCard({task, onUpdated, onDeleted, onEdit, selectedIds, onSelect }: TaskCardProps) {
    const[expanded, setExpanded] = useState(false)
    const[hovered, setHovered] = useState(false)
    const [currentStatus, setCurrentStatus] = useState(task.status)

    const isSelected = selectedIds.has(task.id)
    const isComplete = currentStatus === "completed"
    const currentStatusMeta = STATUS_FILTERS.find(f => f.value === currentStatus)

    async function handleStatusChange(newStatus: TaskStatus, task: Task) {
        task.status = newStatus
        setCurrentStatus(newStatus)
        onUpdated(task)
    }

    return (
        <div className="pl-4 cursor-pointer rounded-lg border-1 border-solid py-5 mb-2 border-blue-black relative transition-shadow "
             style={{
                 boxShadow: expanded ? `0 8px 24px ${colors.lavender}25` : `0 1px 4px ${colors.white}`,
                 transform: expanded ? "translateY(-1px)" : "translateY(0)",}
             }
             onClick={() => onSelect(task.id)}
             onMouseEnter={() => setHovered(!hovered)}
             onMouseLeave={() => setHovered(!hovered)}>

            {/*  Display row  */}
            <div className="flex items-center">
                <div className="flex w-5 h-5 shrink rounded-sm transition-colors cursor-pointer "
                     style={{
                         border: isComplete ? "none" : `2px solid ${colors.blueBlack}`,
                         backgroundColor: isComplete ? "none" : "transparent",
                     }}
                     onClick={(e) => {
                         e.stopPropagation()  // prevent card click from also firing
                         const newStatus = isComplete ? TaskStatus.OPEN : TaskStatus.COMPLETED
                         handleStatusChange(newStatus, task)
                     }}
                >
                    {isComplete && <Check size={24} color={colors.green} strokeWidth={3} />}
                </div>

                <span className="flex pl-4"
                      style={{
                          textDecoration: isComplete ? "line-through" : "none",
                      }}
                >{task.name}</span>

                <div className="relative ml-auto mr-4">
                    <button className="btn btn-primary ml-auto" onClick={(e) => {
                        e.stopPropagation()
                        onEdit(task)
                    }}>
                        <Pencil size={12} /> Edit
                    </button>
                </div>
                <div
                    className="relative "
                    onClick={(e) => e.stopPropagation()}
                    style={{
                        backgroundColor: `${currentStatusMeta?.color}18`,
                        borderRadius: "999px",
                        border: `1.5px solid ${currentStatusMeta?.color}40`,
                    }}
                >
                    <select
                        className="appearance-none pl-6 pr-6 py-1 text-xs font-semibold cursor-pointer bg-transparent outline-none"
                        style={{ color: currentStatusMeta?.color }}  // colors the selected value display
                        value={currentStatus}
                        onChange={(e) => handleStatusChange(e.target.value as TaskStatus, task)}
                    >
                        {STATUS_FILTERS.filter(f => f.value !== undefined).map((filter) => (
                            <option
                                key={filter.label}
                                value={filter.value}
                                style={{ color: colors.blueBlack }}  // force options back to dark neutral
                            >
                                {filter.label}
                            </option>
                        ))}
                    </select>
                    {/* dot on the left */}
                    <span
                        className="absolute left-2 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full pointer-events-none"
                        style={{ backgroundColor: currentStatusMeta?.color }}
                    />

                    {/* chevron on the right */}
                    <ChevronDown
                        size={11}
                        className="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"
                        style={{ color: currentStatusMeta?.color }}
                    />

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
                            onClick={(e) => { e.stopPropagation(); onDeleted(task.id) }}>
                        <Trash2 size={12} />
                        Delete
                    </button>
                </div>
            </div>
        </div>
    )}