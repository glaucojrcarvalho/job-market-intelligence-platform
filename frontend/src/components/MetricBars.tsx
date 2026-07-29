import type { MetricBucket } from '../api/market'

type MetricBarsProps = {
  items: MetricBucket[]
  ariaLabel: string
}

export function MetricBars({ items, ariaLabel }: MetricBarsProps) {
  const maximum = Math.max(...items.map((item) => item.value), 1)

  return (
    <ol className="metric-bars" aria-label={ariaLabel}>
      {items.map((item) => (
        <li key={item.label}>
          <div className="metric-label">
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
          <div className="metric-track" aria-hidden="true">
            <span
              className="metric-fill"
              style={{ width: `${(item.value / maximum) * 100}%` }}
            />
          </div>
        </li>
      ))}
    </ol>
  )
}
