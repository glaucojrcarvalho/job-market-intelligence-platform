import { Link } from 'react-router'

export function NotFoundPage() {
  return (
    <section className="not-found">
      <p className="eyebrow">404</p>
      <h1>This page is not part of the market map.</h1>
      <p>The address may be incorrect or the page may have moved.</p>
      <Link className="button button-primary" to="/">
        Go to overview
      </Link>
    </section>
  )
}
