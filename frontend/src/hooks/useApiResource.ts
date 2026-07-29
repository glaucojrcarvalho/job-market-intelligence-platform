import { useCallback, useEffect, useState } from 'react'

export type ResourceState<T> =
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; message: string }

type ResourceResult<T> = {
  state: ResourceState<T>
  retry: () => void
}

export function useApiResource<T>(
  load: (signal: AbortSignal) => Promise<T>,
): ResourceResult<T> {
  const [attempt, setAttempt] = useState(0)
  const [state, setState] = useState<ResourceState<T>>({ status: 'loading' })

  const retry = useCallback(() => {
    setAttempt((current) => current + 1)
  }, [])

  useEffect(() => {
    const controller = new AbortController()

    setState({ status: 'loading' })
    load(controller.signal)
      .then((data) => {
        if (!controller.signal.aborted) {
          setState({ status: 'success', data })
        }
      })
      .catch((error: unknown) => {
        if (
          controller.signal.aborted ||
          (error instanceof DOMException && error.name === 'AbortError')
        ) {
          return
        }

        setState({
          status: 'error',
          message:
            error instanceof Error
              ? error.message
              : 'The request could not be completed.',
        })
      })

    return () => controller.abort()
  }, [attempt, load])

  return { state, retry }
}
