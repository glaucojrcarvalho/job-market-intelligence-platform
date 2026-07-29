import { Link } from 'react-router'

type FeaturePlaceholderProps = {
  eyebrow: string
  title: string
  description: string
  nextStep: string
}

export function FeaturePlaceholder({
  eyebrow,
  title,
  description,
  nextStep,
}: FeaturePlaceholderProps) {
  return (
    <div className="page-stack">
      <header className="page-header">
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p className="page-lead">{description}</p>
      </header>

      <section className="placeholder-card" aria-labelledby="planned-feature">
        <div className="placeholder-grid" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <div>
          <p className="status-chip">Foundation ready</p>
          <h2 id="planned-feature">This interface is the next delivery step</h2>
          <p>{nextStep}</p>
          <Link className="text-link" to="/">
            Return to the product overview
          </Link>
        </div>
      </section>
    </div>
  )
}
