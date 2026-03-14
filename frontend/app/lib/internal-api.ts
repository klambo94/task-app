import { auth } from "@/auth"

const API_URL = process.env.NEXT_PUBLIC_API

/**
 * Use this in Server Components and Route Handlers.
 * Automatically attaches the NextAuth JWT to the request.
 *
 * Example:
 *   const spaces = await internalFetch("/spaces")
 *   const space = await internalFetch(`/spaces/${id}`, { method: "POST", body: JSON.stringify(data) })
 */
export async function internalFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const session = await auth()

  if (!session?.token) {
    throw new Error("Not authenticated")
  }

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.token}`,
      ...options?.headers,
    },
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({}))
    throw new Error(error?.detail ?? `API error: ${res.status}`)
  }

  return res.json()
}