import MyceliumBackground from "@/app/components/myceliumBackground";
import Link from "next/dist/client/link";


export default function Page() {
    return (
        <main className="landing">
            <MyceliumBackground
                                animated={true} drawIn={true}
                                density="low" opacity={.50}/>

            {/* Noise grain overlay */}
            <div className="grain" aria-hidden="true"/>

            {/* Nav */}
            <nav className="nav">
                <span className="logo">Psinaptic</span>
                <Link href="/auth/login" className="nav-login">Sign in</Link>
            </nav>

            {/* Hero */}
            <section className="hero">
                <div className="hero-eyebrow">
                    <span className="eyebrow-dot"/>
                    <span>Personal & Project Management</span>
                </div>

                <h1 className="hero-title">
                    Where<br/> thoughts <br/> <em>connect</em>
                </h1>

                <p className="hero-sub">
                    Psinaptic maps the network between your ideas, tasks,
                    and projects <br/>
                    Creating an organic structure for the way your mind works.
                </p>

                <div className="hero-actions">
                    <Link href="/auth/login" className="btn-primary">
                        Get started
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                    </Link>
                </div>
            </section>

            {/* Feature row */}
             <section className="features">
                {[
                    { label: "Spaces",  desc: "Organise work into connected spaces" },
                    { label: "Threads", desc: "Granular control over every thread" },
                    { label: "Flow",    desc: "Filter and surface what matters now" },
                ].map((f) => (
                    <div key={f.label} className="feature-card">
                        <span className="feature-label">{f.label}</span>
                        <span className="feature-desc">{f.desc}</span>
                    </div>
                ))}
            </section>
        </main>
    )
}