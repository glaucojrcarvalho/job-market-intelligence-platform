import type { ReactNode } from 'react'

type StatePanelProps = {
  title: string
  message: string
  action?: ReactNode
}

export function LoadingState({
  title = 'Loading',
  message = 'Retrieving the latest available information.',
}: Partial<StatePanelProps>) {
  return (
    <section className="state-panel" aria-live="polite" aria-busy="true">
      <span className="state-spinner" aria-hidden="true" />
      <div>
        <h2>{title}</h2>
        <p>{message}</p>
      </div>
    </section>
  )
}

export function EmptyState({ title, message, action }: StatePanelProps) {
  return (
    <section className="state-panel">
      <span className="state-symbol" aria-hidden="true">
        —
      </span>
      <div>
        <h2>{title}</h2>
        <p>{message}</p>
        {action}
      </div>
    </section>
  )
}

export function ErrorState({ title, message, action }: StatePanelProps) {
  return (
    <section className="state-panel state-panel-error" role="alert">
      <span className="state-symbol" aria-hidden="true">
        !
      </span>
      <div>
        <h2>{title}</h2>
        <p>{message}</p>
        {action}
      </div>
    </section>
  )
}
