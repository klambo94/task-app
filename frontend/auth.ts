import Pool from "pg-pool"
import NextAuth from "next-auth";
import PostgresAdapter from "@auth/pg-adapter";
import Google from "@auth/core/providers/google";

const DATABASE_URL = process.env.DB_URL


const pool = new Pool({
    connectionString: DATABASE_URL
})

export const { handlers, signIn, signOut, auth} = NextAuth({
    adapter: PostgresAdapter(pool),
    providers: [
        Google
    ],
    callbacks: {
        async session({ session, user }) {
            // attach user id to session so we can use it in components
            session.user.id = user.id
            return session
        }
    },events: {
        async createUser({ user }) {
            // fires only on first login (registration)
            // good place to create a default board
            await fetch(`${process.env.TASK_API}/api/boards/init`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: user.id })
            })
        }
    },
    pages: {
        signIn: "/auth/login",  // redirect to our custom login page
        signOut: "/"
    }
})