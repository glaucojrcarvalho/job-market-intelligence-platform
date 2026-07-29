import type { ReactNode } from 'react'

import type { ResourceState } from '../hooks/useApiResource'
import { EmptyState, ErrorState, LoadingState } from './AsyncState'

type PanelStateProps<T> = {
  state: ResourceState<T>
  isEmpty: (data: T) => boolean
  emptyTitle: string
  emptyMessage: string
  errorTitle: string
  onRetry: () => void
  children: (data: T) => ReactNode
}

export function PanelState<T>({
  state,
  isEmpty,
  emptyTitle,
  emptyMessage,
  errorTitle,
  onRetry,
  children,
}: PanelStateProps<T>) {
  if (state.status === 'loading') {
    return <LoadingState message="Retrieving data from the platform API." />
  }

  if (state.status === 'error') {
    return (
      <ErrorState
        title={errorTitle}
        message={state.message}
        action={
          <button className="state-action" type="button" onClick={onRetry}>
            Try again
          </button>
        }
      />
    )
  }

  if (isEmpty(state.data)) {
    return <EmptyState title={emptyTitle} message={emptyMessage} />
  }

  return children(state.data)
}
