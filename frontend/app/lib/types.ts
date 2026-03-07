import {colors} from "@/app/lib/tokens";

export const TaskStatus = {
    OPEN: 'open',
    IN_PROGRESS: 'in_progress',
    COMPLETED: 'completed'
} as const


export type TaskStatus = typeof TaskStatus[keyof typeof TaskStatus]

export const STATUS_FILTERS: {label: string; value: TaskStatus | undefined; color: string}[] = [
    {label: 'All',         value: undefined,                  color: colors.lavender},
    {label: 'Open',        value: TaskStatus.OPEN,        color: colors.pinkPurple},
    {label: 'In Progress', value: TaskStatus.IN_PROGRESS, color: colors.lightPurple},
    {label: 'Completed',   value: TaskStatus.COMPLETED,   color: colors.green}
]

export interface Task {
    id: number
    name: string
    description?: string | null
    status: TaskStatus
    created_at: string
    updated_at: string
}

export interface TaskCreate {
    name: string
    description?: string | null
    status: TaskStatus
}
export interface TaskUpdate {
    id?: number
    name?: string
    description?: string | null
    status?: TaskStatus
}
