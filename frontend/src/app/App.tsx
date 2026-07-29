import { Route, Routes } from 'react-router'

import { AppShell } from './AppShell'
import { CandidateMatchingPage } from '../pages/CandidateMatchingPage'
import { JobExplorerPage } from '../pages/JobExplorerPage'
import { MarketDashboardPage } from '../pages/MarketDashboardPage'
import { NotFoundPage } from '../pages/NotFoundPage'
import { OverviewPage } from '../pages/OverviewPage'

export function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<OverviewPage />} />
        <Route path="market" element={<MarketDashboardPage />} />
        <Route path="jobs" element={<JobExplorerPage />} />
        <Route path="match" element={<CandidateMatchingPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}
