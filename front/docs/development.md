# Development

## Local setup

Use Node.js 22 to match the container build environment.

```sh
npm ci
cp .env.example .env
npm run dev
```

The development server binds to `0.0.0.0:5173`. There is no local API proxy in
`vite.config.ts`; browser requests go directly to `VITE_API_URL`. The backend
must therefore be reachable from the browser and permit credentialed requests
from the development origin.

### Development authentication

Development mode displays credential inputs on the otherwise minimal login
screen. `VITE_LOGIN` and `VITE_PASSWORD` only prefill these inputs; a developer
can also enter the values manually. Submitting calls:

```text
POST auth_router/root_auth
```

The current implementation initializes the development user with ID `2366`
after this request. If the development backend uses another identity model,
update the login implementation before relying on profile-specific behavior.

Production mode does not show the credential fields and uses the OAuth redirect
route.

## Working on a feature

### Add a route-level page

1. Create the view below the relevant feature directory in `src/views/`.
2. Add a lazy-loaded named route in `src/router/index.ts`.
3. Add `meta.breadcrumbs` when the page has a parent trail.
4. Add its navigation entry in `src/assets/static/navLinks.ts`, if needed.
5. If gallery cards need custom parameters, extend
   `src/router/uniqueRoutesHandle.ts`.
6. If the page caches shared API data, add a typed key to `viewsData` rather
   than creating component-global state.

Route names, not literal paths, are used throughout the UI. Treat existing route
names as public frontend identifiers.

### Add a content-backed section

For sections based on the common article API:

1. Confirm the numeric section ID with the backend.
2. Add the mapping to `src/assets/static/sectionTips.ts`.
3. Reuse `LayoutPostsPreview` for standard list/filter/pagination behavior.
4. Reuse `PostPreview` and `PostInner` for article details where the shared
   layout is suitable.
5. Add the list type to `DataState` in `src/stores/viewsData.ts` if it should be
   cached.
6. Add list and detail routes and, if applicable, a tag-filter route.

Do not silently repurpose an existing section ID. Several pages, editor
permissions, and backend schemas depend on these values.

### Add or change an admin field

The backend response from `editor/add/{sectionId}` or
`editor/rendering/{articleId}` defines most editor fields. The frontend maps
metadata to controls in `AdminElementEditorFieldRenderer.vue`.

Before adding a new input component, check whether the field fits an existing
case:

| Metadata                       | Control                |
| ------------------------------ | ---------------------- |
| string/int                     | Basic input            |
| string field containing `text` | Text editor/textarea   |
| date-like string               | Date picker            |
| string/bool with `values`      | Select                 |
| `search_by_uuid(s)`            | User search            |
| `areaSearch`                   | Department search      |
| `all_tags` / `vision`          | Tag-style multi-select |
| `reports`                      | Repeated report fields |

Files are managed separately from scalar field values. Keep the upload,
embedded-link, and deletion endpoints consistent with the editor lifecycle.

### Change navigation or access

- Main and utility navigation: `src/assets/static/navLinks.ts`
- Editor navigation groups: `src/assets/static/adminSections.ts`
- Frontend feature switches: `src/assets/static/featureFlags.ts`
- Route guards: `src/router/index.ts`
- Role-derived UI state: `src/stores/userData.ts`

Any access-control change must also be enforced by the backend. Hiding a route or
button in Vue is not an authorization boundary.

## Code conventions

- Use the `@/` alias for imports rooted at `src/`.
- Keep route components in `src/views/` and reusable components in
  `src/components/`.
- Put cross-view reactive logic in `src/composables/` and pure helpers in
  `src/utils/`.
- Define API/domain shapes under `src/interfaces/` instead of adding untyped
  response objects to components.
- Cancel long-lived GET requests on unmount with `AbortController`.
- Use the shared `Api` utility so session headers and global 401/502 handling are
  preserved.
- Use the shared toast composable and response helpers for mutation feedback.
- Preserve the existing 4-space editor indentation. Prettier is configured for
  single quotes, no semicolons, and a 100-character line width.

`npm run lint` includes `--fix`, and `npm run format` writes files. Review the
resulting diff after either command.

## Testing

### Unit and component tests

Vitest uses `jsdom` and discovers `*.spec.ts` files. Existing tests cover utility
functions, search-list rendering, header notifications, and notification
broadcast behavior.

```sh
npm test -- --run
npm run coverage
```

Current known issues with the all-project command:

- `eTe-test/example.spec.ts` is a fully commented Playwright placeholder, but
  Vitest still discovers it and reports that it contains no suite.
- `SearchList` currently renders an empty `<ul>` for an empty array, while one
  test expects no `<ul>`.
- A nested `.kilo/worktrees/...` checkout may also be discovered when present,
  causing duplicate suites. It is not excluded in `vite.config.ts`.

These are test-configuration or implementation issues, not setup requirements.
Do not interpret a failing full run as a missing dependency without inspecting
the reported suite paths.

### Browser tests

Playwright is configured in `playwright.config.ts` for Chromium, Firefox, and
WebKit:

```sh
npx playwright install
npx playwright test
```

The configured `webServer` block is commented out, so start the application
separately and make browser tests navigate to the desired URL. The only checked-in
example is currently commented and does not exercise the application.

### Validation before a change is merged

At minimum, run:

```sh
npm run type-check
npm run build-only
```

Run the relevant Vitest file(s) for the area being changed, then document any
unrelated known failures in the handoff.

## Build and deployment

```sh
npm run build
```

The command runs `vue-tsc --build` and `vite build` in parallel and writes
assets to `dist/`. Source maps are enabled.

The deployment server needs SPA fallback routing. It should serve existing
static files normally and send `index.html` when a frontend route does not map
to a file.

The current Dockerfile installs dependencies, creates `dist/`, and starts
`npm run preview`. Although its final working directory is `/app/dist`, npm
resolves the project manifest and dependencies from the parent `/app` directory.
The image therefore starts successfully. Vite preview is intended for build
verification; a hardened production deployment should use a dedicated static
web server with an explicit SPA fallback.

## Troubleshooting

### The login screen never completes

- Verify `VITE_API_URL` and backend CORS/credential settings.
- Confirm the browser has or can receive a `session_id` cookie.
- In development, confirm the test credentials are accepted by
  `auth_router/root_auth`.
- In production, confirm the OAuth domain and client ID were present at build
  time.

### API calls suddenly return to the login screen

The shared API client treats a 401 as an expired session, clears frontend state
and cookies, and shows the login shell. Inspect the failing request and renew the
backend session.

### The maintenance screen appears

The shared API client redirects primary API 502 responses to `/inservice`. That
page polls `/health_check`; investigate backend availability first.

### A direct URL works through navigation but 404s after refresh

Configure the web server with an SPA fallback to `index.html`. Vue Router uses
history mode, so route paths do not correspond to files in `dist/`.

### A feature is missing from the sidebar

Check both the user's role object and `src/assets/static/featureFlags.ts`. The
admin sidebar applies both when constructing its navigation groups.

### A page displays the wrong content

Confirm its entry in `src/assets/static/sectionTips.ts`. Article list endpoints
use those numeric IDs directly.
