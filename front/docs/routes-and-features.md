# Routes and features

The router is defined in `src/router/index.ts`. This document groups routes by
product area; it intentionally describes patterns instead of duplicating every
breadcrumb or component import.

## Public and shell-special routes

| Path          | Route name  | Purpose                                                    |
| ------------- | ----------- | ---------------------------------------------------------- |
| `/`           | `home`      | Content-driven intranet home page                          |
| `/user/auth`  | `auth`      | Login view (the app shell also renders it when logged out) |
| `/oauthRedir` | `oauthPage` | Starts the production OAuth redirect                       |
| `/vcard/:id`  | `vcard`     | Virtual business card with a dedicated shell               |
| `/inservice`  | `inservice` | Backend-maintenance status page                            |

Most content routes are visible only through the authenticated application shell,
although only the admin area has explicit per-route role guards. Backend access
control remains authoritative.

## About the company

| Path pattern                                                     | Feature                                |
| ---------------------------------------------------------------- | -------------------------------------- |
| `/about`                                                         | Company overview                       |
| `/about/company-history[/:id]`                                   | Company history and chapter view       |
| `/about/our-people[/:id]`                                        | People directory and interviews        |
| `/about/year-results`                                            | Employee recognition/board of honor    |
| `/about/blogs`, `/about/blogs/:id`, `/about/blogs/:authorId/:id` | Blog authors, author feed, and article |
| `/about/fornewworker`                                            | New-employee guide                     |
| `/about/birthdays`                                               | Employee birthdays                     |
| `/about/newworkers`                                              | New employees                          |
| `/about/vacancies`                                               | Open vacancies/referral page           |
| `/about/calendar[/:targetId]`                                    | Company event calendar                 |

### Training center

The `/about/trainingcenter` family includes the landing page, e-courses,
conducted training and feedback, announcements, excursions, literature, and the
1C memo. E-course and conducted-training detail pages use an `:id` parameter.

### Safety

`/about/safetytechnics` is the section landing page. Child routes cover COVID,
fire/evacuation, and factory safety information.

## Services

| Path                                        | Purpose                                                |
| ------------------------------------------- | ------------------------------------------------------ |
| `/services/postcard`                        | Create and email a greeting card                       |
| `/services/chatgpt`                         | Internal GPT chat, file analysis, and image generation |
| `/services/experience`                      | Supply references grouped by factory                   |
| `/services/experience/:factoryId`           | Sectors for a factory                                  |
| `/services/experience/:factoryId/:sectorId` | Documents for a factory sector                         |

These routes open external systems instead of rendering local views:

- `/services/selectionTep` — TEP equipment selection;
- `/services/selectionReg` — regulator equipment selection;
- `/services/deepseek` — internal DeepSeek UI;
- `/services/cert` — internal certificate service.

The redirects are currently hard-coded in the router rather than derived from
environment variables.

## News and media

| Path pattern                        | Feature                              |
| ----------------------------------- | ------------------------------------ |
| `/news/actual`                      | Current news list                    |
| `/news/actual/tag/:tagId`           | Current news filtered by tag         |
| `/news/actual/:id`                  | Current news article                 |
| `/news/corpnews`                    | Organizational appointments/news     |
| `/news/corpnews/sinerteam`          | Organizational-development team view |
| `/news/corpnews/:id`                | Organizational news article          |
| `/news/gazette`                     | Corporate newspaper archive          |
| `/gallery/videoInterviews[/:id]`    | Video interviews                     |
| `/gallery/videoManagement[/:id]`    | Management interviews                |
| `/gallery/videoreports[/:id]`       | Video reports                        |
| `/gallery/videoreportsByTag/:tagId` | Video reports filtered by tag        |
| `/gallery/filmsEmk[/:id]`           | EMK creative-group films             |
| `/gallery/filmsEmk/tag/:tagId`      | Films filtered by tag                |

## Factory guide

| Path                                           | Route name       | Purpose                  |
| ---------------------------------------------- | ---------------- | ------------------------ |
| `/gallery/factories`                           | `factories`      | Factory list             |
| `/gallery/factories/reports/:id`               | `factoryReports` | Factory reports          |
| `/gallery/factories/tours/:id`                 | `factoryTours`   | Available factory tours  |
| `/gallery/factories/tours/:factory_id/:tourId` | `factoryTour`    | Interactive factory tour |

Factory data is prefetched into its own Pinia store when one of these routes is
visited.

## Internal communications

| Path pattern                                                     | Feature                          |
| ---------------------------------------------------------------- | -------------------------------- |
| `/communications/officialevents[/:id]`                           | Official photo events            |
| `/communications/corpevents/`                                    | Corporate events                 |
| `/communications/corpevent/:id`                                  | Corporate event detail           |
| `/communications/corpevents/:tagId`                              | Corporate events filtered by tag |
| `/communications/corplife/` and `/communications/corplife/:id`   | Corporate life gallery           |
| `/communications/announces/` and `/communications/announces/:id` | Event announcements              |
| `/communications/contest/`                                       | Competitions                     |
| `/gallery/partners/` and `/gallery/partners/:id`                 | Partner offers                   |
| `/gallery/care/` and `/gallery/care/:id`                         | Charity projects                 |

## EMK Capital and points

| Path pattern                  | Feature                                   |
| ----------------------------- | ----------------------------------------- |
| `/about/capitalEmk/about`     | Explanation of the points/capital program |
| `/about/capitalEmk/merch`     | Merchandise catalog                       |
| `/about/capitalEmk/merch/:id` | Merchandise detail and purchase flow      |
| `/user/:id`                   | Employee profile and point transfer       |
| `/user/ideas/`                | Current user's ideas                      |
| `/user/ideas/new`             | New idea submission                       |

The points data prefetch loads available actions, user history, and activity
definitions when `featureFlags.pointsSystem` is enabled.

## Administration

All routes below call the role endpoint before entry and redirect to `home` when
no role object is returned. Some pages apply narrower checks inside the page or
sidebar.

| Path                      | Route name              | Purpose                                                |
| ------------------------- | ----------------------- | ------------------------------------------------------ |
| `/admin`                  | `admin`                 | Editor navigation                                      |
| `/admin/:id`              | `adminBlockInner`       | Items in a content section                             |
| `/admin/:id/new`          | `adminElementInnerAdd`  | Create a section item                                  |
| `/admin/:id/:elementId`   | `adminElementInnerEdit` | Edit a section item                                    |
| `/admin/notifications`    | `notificationBroadcast` | Broadcast notifications; requires flag and `PeerAdmin` |
| `/admin/visibility`       | `visibilityArea`        | Visibility-area editor                                 |
| `/admin/scoreAdmin`       | `pointsAdministrator`   | Points-system administration                           |
| `/admin/pointsmoderation` | `pointsModeration`      | Points moderation                                      |
| `/admin/curatorhistory`   | `curatorHistory`        | Curator transaction history                            |
| `/admin/roots`            | `roots`                 | Editor and GPT permissions                             |

### Route-order caution

The router contains dynamic `/admin/:id` routes alongside fixed paths such as
`/admin/visibility`. Vue Router ranks static segments ahead of dynamic ones, but
new admin routes should still use a distinct static path and a unique route name.

## Authenticated service redirects

The following routes check for a `session_id` cookie before redirecting to
backend services:

| Path                   | Destination behavior                            |
| ---------------------- | ----------------------------------------------- |
| `/exhibition`          | Opens the exhibition contact-collection service |
| `/exhibition_app`      | Opens the exhibition app service                |
| `/auth_router/argconf` | Opens the ARG configuration service             |

When no session is present, the user is sent through the home/login flow with a
`reroute` query value. `App.vue` accepts that post-login redirect only when the
value contains the trusted `https://intranet.emk.ru` origin.
