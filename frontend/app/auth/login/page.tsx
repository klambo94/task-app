import { signIn } from "@/auth"
import MyceliumBackground from "@/app/components/myceliumBackground";

export default function LoginPage() {
    return (
        <main className={`landing`}>
            <MyceliumBackground
                animated={true} drawIn={true}
                density="low" opacity={.50}/>
            {/* Noise grain overlay */}
            <div className="grain" aria-hidden="true"/>
            <div className="sign-in-form">
                <h1 className="logo">Sign in to Psinaptic</h1>
                <p className="heading">Collaborative workspace for your team</p>
                <form action={async () => {
                    "use server"
                    await signIn("google", { redirectTo: "/api/spaces" })
                }}>
                    <button className="btn-primary" type="submit">Continue with Google</button>
                </form>
                <div className="sub-heading">
                    <p>Private Policy stub</p>
                </div>
            </div>
        </main>
    )
}