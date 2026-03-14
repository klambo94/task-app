import { DefaultSession } from "next-auth"
import { JWT } from "next-auth/jwt"

declare module "next-auth" {
  interface Session {
    token?: string  // plain HS256 JWT for FastAPI
    user: {
      id: string
    } & DefaultSession["user"]
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    picture?: string | null
    apiToken?: string  // minted HS256 JWT
  }
}