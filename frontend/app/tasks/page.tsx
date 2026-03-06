import {getTasks} from "@/app/lib/api";
import TaskPageClient from "./TaskPageClient";
import {TaskStatus} from "@/app/lib/types";

export default async function TaskPage() {
    const tasks = await getTasks()
    return  <TaskPageClient initTasks={tasks}/>
}