import {getTasks} from "@/app/lib/api";
import TaskPageClient from "./TaskPageClient";
import {auth} from "@/auth";
import {redirect} from "next/navigation";
export const dynamic = "force-dynamic"

export default async function TaskPage() {
    const session = await auth()
    if (!session) redirect("/auth/login")

    const tasks = await getTasks()
    return  <TaskPageClient initTasks={tasks}/>
}