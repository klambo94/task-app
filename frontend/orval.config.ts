import { defineConfig } from "orval"

export default defineConfig({
  psinaptic: {
    input: {
      target: process.env.API_URL ?? "http://localhost:8000/openapi.json",
    },
    output: {
      mode: "tags-split",
      target: "app/lib/generated",
      schemas: "app/lib/generated/model",
      client: "react-query",
      httpClient: "axios",
      override: {
        mutator: {
          path: "app/lib/axios.ts",
          name: "axiosInstance",
        },
      },
    },
  },
})