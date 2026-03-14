import axios from "axios"
import { getSession } from "next-auth/react"

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API,
})

// Attach JWT to every request automatically
instance.interceptors.request.use(async (config) => {
  const session = await getSession()
  if (session?.token) {
    config.headers.Authorization = `Bearer ${session.token}`
  }
  return config
})

// Orval expects a named export called axiosInstance
export const axiosInstance = <T>(config: Parameters<typeof instance>[0]): Promise<T> => {
  return instance(config).then((res) => res.data)
}

export default instance
