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

The frontend runs at `http://localhost:3000` by default. The API base URL defaults to
`http://localhost:8000` and can be changed with `VITE_API_BASE_URL`.

The backend does not yet configure CORS. Cross-origin API requests from the standalone frontend
will be enabled in the later Docker Compose integration task. The foundation routes do not issue
API requests.

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
| `/market` | Foundation placeholder for the market dashboard |
| `/jobs` | Foundation placeholder for the job explorer |
| `/match` | Foundation placeholder for candidate matching |

The placeholder routes define navigation and page boundaries without claiming that later product
features are implemented.
