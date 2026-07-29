import { NavLink, Outlet } from 'react-router'

import { apiBaseUrl } from '../api/client'

const repositoryUrl =
  'https://github.com/glaucojrcarvalho/job-market-intelligence-platform'

const navigation = [
  { to: '/', label: 'Overview', end: true },
  { to: '/market', label: 'Market' },
  { to: '/jobs', label: 'Jobs' },
  { to: '/match', label: 'Match' },
]

export function AppShell() {
  return (
    <div className="app">
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>

      <header className="site-header">
        <div className="shell header-inner">
          <NavLink className="brand" to="/" aria-label="Market Intelligence home">
            <span className="brand-mark" aria-hidden="true">
              MI
            </span>
            <span>
              <strong>Market Intelligence</strong>
              <small>Software engineering</small>
            </span>
          </NavLink>

          <nav aria-label="Primary navigation">
            <ul className="nav-list">
              {navigation.map((item) => (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    end={item.end}
                    className={({ isActive }) =>
                      isActive ? 'nav-link nav-link-active' : 'nav-link'
                    }
                  >
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </header>

      <div className="data-notice" role="note">
        <div className="shell data-notice-inner">
          <span className="notice-icon" aria-hidden="true">
            i
          </span>
          <p>
            Data comes from records stored in this instance and may be manually
            uploaded or synthetic. It is not live or complete market coverage.
          </p>
        </div>
      </div>

      <main className="shell main-content" id="main-content" tabIndex={-1}>
        <Outlet />
      </main>

      <footer className="site-footer">
        <div className="shell footer-inner">
          <p>
            Open-source market intelligence, currently under active
            development.
          </p>
          <nav aria-label="Developer resources">
            <a href={`${apiBaseUrl}/docs`}>API docs</a>
            <a href={`${apiBaseUrl}/health`}>Health</a>
            <a href={repositoryUrl}>Repository</a>
            <a href={`${repositoryUrl}/blob/main/docs/03-architecture.md`}>
              Architecture
            </a>
          </nav>
        </div>
      </footer>
    </div>
  )
}
