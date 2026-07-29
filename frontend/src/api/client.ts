const DEFAULT_API_BASE_URL = 'http://localhost:8000'

function normalizeBaseUrl(value: string): string {
  return value.replace(/\/+$/, '')
}

export const apiBaseUrl = normalizeBaseUrl(
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL,
)

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function requestJson<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...init?.headers,
    },
  })

  if (!response.ok) {
    throw new ApiError(
      response.status,
      `The API request failed with status ${response.status}.`,
    )
  }

  return (await response.json()) as T
}
