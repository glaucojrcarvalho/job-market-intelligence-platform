# Frontend

React and TypeScript single-page application for the public product interface.

## Requirements

- Node.js 24 LTS
- npm 11 or later

## Local development

Install the locked dependencies:

```bash
cd frontend
npm ci
```

Create an optional local environment file:

```bash
cp .env.example .env.local
```

Start the development server:

```bash
npm run dev
```

The frontend runs at `http://localhost:3000` by default. The API base URL defaults to `/api`,
which the Vite development server proxies to `http://localhost:8000`. It can be changed with
`VITE_API_BASE_URL`. If the local API uses a different origin, configure `API_PROXY_TARGET`.

The local proxy lets the standalone dashboard use the API without broadening backend CORS.
Production API routing and environment-scoped CORS will be finalized in the later Docker Compose
integration task.

## Scripts

```bash
npm run lint
npm run typecheck
npm run build
npm run preview
```

Frontend tests and their CI quality gate are intentionally deferred to the dedicated frontend
quality task.

## Routes

| Route | Current state |
| --- | --- |
| `/` | Product overview and developer access |
| `/market` | API-backed market dashboard |
| `/jobs` | Foundation placeholder for the job explorer |
| `/match` | Foundation placeholder for candidate matching |

The placeholder routes define navigation and page boundaries without claiming that later product
features are implemented.
