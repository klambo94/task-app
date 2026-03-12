import { signIn } from "@/auth"

export default function LoginPage() {
    return (
        <main>
            <h1>Sign in to Psinaptic</h1>
            <form action={async () => {
                "use server"
                await signIn("google", { redirectTo: "/tasks" })
            }}>
                <button type="submit">Continue with Google</button>
            </form>
        </main>
    )
}