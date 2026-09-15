# Проект Intranet2.0 — Полное техническое описание

Корпоративный портал (интранет) компании ЭМК. Многосервисный стек на Docker Compose.
Бэкенд — FastAPI (Python 3.13), фронтенд — Vue 3 + Vite (Node 22), PostgreSQL 15,
Redis, Elasticsearch, мониторинг (Prometheus + Grafana + Loki + Promtail). Вход — nginx reverse-proxy с TLS.

---

## 1. Общая архитектура и данные

### 1.1. docker-compose.yaml (сеть `app-network`, bridge)

| Сервис | Образ | Порт (host) | Роль |
|---|---|---|---|
| nginx | nginx:alpine | 80:80, 443:443 | reverse-proxy, вход |
| postgres | postgres:15-alpine | 127.0.0.1:5432 | БД (pdb, user/pswd) |
| elasticsearch | elasticsearch:9.1.0 | 127.0.0.1:9200,9300 | поиск |
| redis | redis:alpine | 127.0.0.1:6379 | кэш/сессии (requirepass pswd) |
| fastapi | build ./code | 127.0.0.1:8000 | API |
| frontend | build ./front | 127.0.0.1:5173 | Vue SPA (vite preview) |
| prometheus | prom/prometheus | 9090 | метрики |
| grafana | grafana/grafana | 3000 | дашборды |
| loki | grafana/loki | 3100 | хранение логов |
| promtail | grafana/promtail | 9080 (внутр.) | сбор логов docker |

- Тома-бинды: `prometheus_data`, `grafana_data`, `loki_data` → локальные папки.
- Внутренние сервисы слушают только localhost; публичные 9090/3000/3100 защищаются iptables.
- Код `code/` подмонтирован bind-mount (hot reload).

### 1.2. nginx/default.conf
- Порт 80 → редирект 301 на HTTPS.
- HTTPS: `server_name ${NGINX_HOST}` (из env DOMAIN), SSL-сертификаты из `nginx/ssl/` (gitignored),
  `client_max_body_size 1024M`, `underscores_in_headers on`.
- `location /` → `http://frontend:5173`
- `location /api/` → `http://fastapi:8000`
- Страница техработ `/50x.html` с картинкой `cat502.jpg` для 404/502/503/504.

### 1.3. .env.example
- `HOST`, `DOMAIN` — внешний URL/домен
- `user`, `pswd` — PostgreSQL-учётка и общий пароль (Redis, ES, LDAP-код)
- `LDAP_SERVER=ldaps://imp.int:636`, `LDAP_DOMAIN=imp.int`
- `mail_server`, `mail_login`, `mail_password` — SMTP рассылка

### 1.4. Мониторинг и логи
- **Prometheus** собирает метрики `fastapi_async:8000/metrics` (от `prometheus-fastapi-instrumentator`).
- **Loki** (TSDB, retention 7 дней) + **Promtail** собирает логи ТОЛЬКО контейнера `fastapi_async`.

### 1.5. Скрипты обслуживания
- `reset.sh` — git pull dev + перезапуск fastapi.
- `reset_front.sh` — git pull main + пересборка frontend.
- `clear.sh` — down + prune + очистка данных всех БД + up.
- `clear_files.sh` — то же без prune/up.
- `total_reboot.sh` — полный сброс и пересборка всего стека.

### 1.6. Firewall (`firewall/`)
- `setup_firewall.sh` — iptables-цепочка DOCKER-USER: открыть 22/80/443 всем; для админ-IP из
  `admin_ip.txt` открыть порты 5432, 6379, 8000, 9200, 9300, 27017; остальное DROP.
- `AdminPanel.py` — добавление админ-IP (с проверкой кредов), `admin_ip.txt`.

### 1.7. pSQL/createView.sql
- Представление `NewUsers`: пользователи, зарегистрированные за последние 2 недели.

---

## 2. Бэкенд (`code/`) — FastAPI

Приложение `main.py` (~2400 строк), `app = FastAPI(title="Intranet2.0 API DOCS", version="2.0.0")`.
Swagger на `/api/docs`, схема `/api/openapi.json`. Все роутеры монтируются под префиксом **`/api`**.

### 2.1. Подключаемые роутеры

| Роутер | Префикс `/api` | Теги |
|---|---|---|
| users_router | `/users` | Пользователь, Битрикс24 |
| depart_router | `/departments` | Департамент, Битрикс24 |
| usdep_router | `/users_depart` | Пользователь-Департамент, Битрикс24 |
| section_router | `/section` | Разделы |
| article_router | `/article` | Статьи, Битрикс24 |
| tag_router | `/tags` | Тэги |
| file_router | `/file` | Файлы |
| search_router | `/elastic` | Поиск по тексту |
| b24_router | `/b24` | Битрикс24 |
| vcard_app | `/vcard` | VCard, Битрикс24 |
| C_app | `/1c-help` | 1С справка |
| auth_router | `/auth_router` | Авторизация |
| compress_router | `/compress_image` | Компрессия изображений |
| idea_router | `/idea` | Есть Идея!, Битрикс24 |
| idea_pdf_router | `/idea_pdf` | PDF идей |
| editor_router | `/editor` | Редактор |
| fieldsvisions_router | `/fields_visions` | Области видимости |
| peer_router | `/peer` | Система эффективности (баллы) |
| roots_router | `/roots` | Права пользователя |
| store_router | `/store` | Магазин мерча |
| ai_router | `/ai` | GPT |
| open_router | `/open` | Открытые ссылки |

Статика: `/api/tours`, `/api/files`, `/api/user_files`, `/api/vcard_files`.

### 2.2. Ключевые эндпоинты main.py
- GET `/api/health_check` — health-check для фронта
- PUT `/api/full_elastic_dump` — дамп User/Structure/Article в ES
- GET `/api/full_search/{keyword}` — полнотекстовый поиск через ES
- PUT `/api/total_background_task_update` — фоновая загрузка всех данных из B24
- PUT `/api/total_update` — полное обновление (tables + 7 сущностей)
- GET `/api/users_update/`, `/api/art_update/` — обновление сущностей
- WS `/ws/progress/{upload_id}` — прогресс загрузки файла
- GET `/api/scheduler/status`, POST `/api/scheduler/run-now`

### 2.3. Авторизация и middleware
- Глобальный http-middleware для всех `/api`-запросов:
  1. Список `open_links` — публичные пути пропускаются без авторизации.
  2. Из cookie или заголовка `session_id` создаётся `AuthService`, валидируется сессия.
  3. Нет session_id или невалидная → 401 с `auth_url`.
  4. При успехе в `request.state` кладётся `user_id`, `user_info`, `session_id`, `access_token`.
  5. После ответа — скользящее окно сессии в Redis, переустановка cookie.
- Авторизация через OAuth Bitrix24 (`/auth_router/auth`) + root_auth (логин/пароль через POST-форму portal.emk.ru).
- CORS-мидлвейр закомментирован (полагается на прокси-уровень).

### 2.4. Подключения (инициализация)
- **PostgreSQL**: `postgresql+asyncpg://{user}:{pswd}@postgres/pdb`, pool 25+25, SQLAlchemy async.
- **Redis**: `redis:6379`, db 0, пароль pswd — сессии (`RedisStorage`).
- **Elasticsearch**: `http://elasticsearch:9200`, basic_auth `elastic`/pswd, индексы user/articles/departs.
- **Scheduler**: `aioscheduler` — `daily_check` (07:00), `weekly_check` (сб), очередь отложенных задач в Redis.
- **Prometheus**: `Instrumentator().instrument(app).expose(app)` — `/metrics`.
- Загрузка файлов: `max_upload_size` 2 ГБ, прогресс через WebSocket.

---

## 3. Бэкенд — слои `src/`

Слои (нестандартная терминология):
- **`src/model/`** — бизнес-фасад: классы-сервисы сущностей + FastAPI-роутеры.
- **`src/base/pSQL/models/`** — SQLAlchemy ORM-модели (declarative Base).
- **`src/base/pSQL/objects/`** — репозитории (`*Model`), выполняют SQL/ORM-запросы.
- **`src/base/Elastic/`** — поиск.
- **`src/base/`** — инфраструктура: B24 (Bitrix24), RedisStorage, JSON-конфиги.
- **`src/services/`** — функциональные сервисы.

Паттерн: endpoint → класс сущности/сервиса → репозиторий (`*Model`) → `AsyncSession`
(зависимость `get_async_db`). Многие данные хранятся в **JSONB-колонке `indirect_data`**
(мутация требует `flag_modified`).

### 3.1. src/model/
- **User** (`/users`) — синхронизация с B24, фото, именинники/новички/юбилеи, лайки, Excel-метрики, поздравления. Регистратор отложенных задач `TASK_HANDLERS`.
- **Department** (`/departments`) — департаменты из B24, эталонная зависимость `get_user_id_by_session_id`.
- **UsDep** (`/users_depart`) — связи пользователь↔департамент.
- **Article** (`/article`) — самый большой файл: нормализация статей из B24 с спец-обработкой по `section_id` (блоги, видео, новости, конкурсы и т.д.), файлы, выгрузка, лайки.
- **Tag** (`/tags`) — теги из `current_tags.json`.
- **Section** (`/section`) — разделы из `sections.json`.
- **File** (`/file`) — файлы/фото пользователей, загрузка с прогрессом `UPLOAD_PROGRESS`.

### 3.2. src/base/pSQL/models/ (таблицы)
`users`, `departments`, `section`, `article`, `usdep`, `tags`, `filesdb`, `userfiles`,
`likes`, `views`, `artvis`, `fieldvision`, `uservisionsroot`, `activities`, `activeusers`,
`moders`, `PeerHistory`, `Roots` (root_token JSONB + user_points).

Ключевые поля:
- **User**: id, uuid, active, ФИО, email, phone, личное, `indirect_data` (JSONB), photo_file_id.
- **Article**: id, section_id, name, active, preview/content_text, content_type, даты, `indirect_data`.
- **Roots**: user_uuid, `root_token` (JSONB), user_points (баллы).

### 3.3. src/base/pSQL/objects/ (репозитории)
- **UserModel** — upsert из B24, поиск, праздники (birthday/anniversary, маппинг YEARS_ID), области видимости.
- **DepartmentModel**, **UsDepModel**, **SectionModel**, **ArticleModel** (фильтры: год/тег/offset/limit), **LikesModel**, **ViewsModel**, **TagsModel**, **FilesDBModel**, **UserFilesModel**, **FieldvisionModel**, **UservisionsRootModel** (CTE-дерево департаментов).
- **ActivitiesModel**, **ActiveUsersModel**, **PeerUserModel** (ядро баллов, ~1200 строк: подтверждение, начисление, транзакции, авто-баллы за ДР/новичков/идеи), **RootsModel** (RBAC через root_token), **MerchStoreModel** (покупка мерча за баллы).
- **App.py** — `AsyncSessionLocal`, `get_async_db()`, таблица `NewUser` (Core).

### 3.4. src/base/Elastic/
- **App.py** — `search_everywhere(keyword)` — комбинированный поиск по индексам articles + user (буст, fuzzy, phrase, highlight) → секции «Пользователи»/«Контент».
- **UserSearchModel** (`user`) — ФИО/email/phone/город, кастомные анализаторы (edge_ngram).
- **ArticleSearchModel** (`articles`) — title/preview/content с highlight.
- **StuctureSearchmodel.py** (`departs`) — дерево подразделений (BFS по 8 уровням).

### 3.5. src/base/B24.py и RedisStorage.py
- **B24** — webhook-токены на каждый метод (захардкожены), user.get/department.get/lists.element.get,
  кастомные pub-endpoints (getBfileById.php, getLikes.php), отправка идей + запуск БП. `/b24/calendar/{from}/{to}`.
- **RedisStorage** — save/get/delete session (SETEX, JSON), TTL, set-операции (`user_sessions:{user_id}`).

### 3.6. src/services/
- **Auth.py** — OAuth Bitrix24 + root_auth, TTL: access 1h, refresh 30d, session 7d, sliding 15min.
- **Peer.py** (`/peer`) — балльная система: действия, валидация модератором, кураторы, админы, перевод баллов, история, топ.
- **Roots.py** (`/roots`) — права: EditorAdmin/EditorModer, первичные админы (id 2366, 2375, 4133), GPT-лицензии.
- **FieldsVisions.py** (`/fields_visions`) — области видимости (VisionAdmin/VisionRoots).
- **Editor.py** (`/editor`, ~1440 строк) — конструктор статей по шаблонам `fields.json`/`patterns.json`, рендеринг, авторы, синхронизация ES.
- **AIchat.py** (`/ai`) — прокси на `gpt.emk.ru`, стриминг, multipart.
- **Idea.py** + **IdeaPFD.py** — банк идей, генерация PDF из шаблона docx.
- **MerchStore.py** (`/store`) — покупка мерча, уведомление на почту.
- **VCard.py** (`/vcard`) — электронные визитки (.vcf), QR-код.
- **SendMail.py** — SMTP-рассылки (поздравления, новичкам, покупки, баг-репорты).
- **Comporession.py** (`/compress_image`) — ресайз PIL (357×204, 700×1024, 359×493).
- **Chelp.py** (`/1c-help`) — статичная справка 1С из `1c.json`.
- **LogsMaker.py** — логгирование в файл + JSON для Loki.
- **scheduler.py** — aioscheduler + очередь отложенных задач в Redis.

### 3.7. RBAC (права в `Roots.root_token`)
Ключи: `PeerAdmin`, `PeerModer`, `PeerCurator`, `VisionAdmin`, `VisionRoots`, `EditorAdmin`, `EditorModer`, `GPT_gen_access`.

### 3.8. Магические id (важно)
- Разделы: 9 заводы, 13 Наши люди, 14 Доска почёта, 15 Блоги, 31/51 новости, 32 оргразвитие,
  41 гид по предприятиям, 42/52 галерея, 53 афиша, 55 благотворительность, 56 мерч, 71 конкурсы,
  111 вакансии, 172 тренинги, 175 литература.
- Активности Peer: 1 ДР, 3 новички, 4 идеи, 5 новость, 6 лучший сотрудник, 7–16 годовщины/юбилеи, 17 достижения.

---

## 4. Фронтенд (`front/src/`) — Vue 3 SPA

Стек: Vue 3.5, Vue Router 4, Pinia 3, Axios, Bootstrap 5, PrimeVue 4, Swiper 11, Quill,
vee-validate, markdown-it, sanitize-html, js-cookie. Сборка Vite 6 + TS + SCSS.

### 4.1. main.ts / App.vue
- Глобально: `v-lazy-load` (IntersectionObserver), VueDatePicker, FileUpload (PrimeVue), Pinia, Router, ToastService.
- App.vue: три режима (vcard / inservice / обычный layout в PullToRefresh).
- Если не залогинен и загрузка завершена → `AuthPage`.
- Инициализация сессии: читает cookie `session_id` → `users/find_by_session_id/{key}`.
- Watcher на [isLogin, route.name] — предзагрузка секций (score/calendar/user/blogs/factoryGuid), лимит GPT.
- Тёмный режим: класс `.dark-mode` + localStorage `darkMode`.

### 4.2. Router (`router/index.ts`, ~90 маршрутов)
- Ленивая загрузка, `scrollBehavior`, `linkActiveClass`.
- Защита админки через guard `beforeEnter` → `roots/get_root_token_by_uuid`.
- Классы маршрутов: `/` (home), `/about/*` (компания, история, люди, блоги, УЦ, ТБ, календарь...),
  `/gallery/*`, `/news/*`, `/communications/*`, `/services/*`, `/user/*`, `/admin/*`, `/vcard/:id`, `/oauthRedir`.
- Детальные страницы — общий компонент **PostPreview.vue** / **PostInner**.
- `uniqueRoutesHandle.ts` — построение параметров маршрута для ссылок из слайдов.

### 4.3. Pinia-сторы (`stores/`)
- **userData** — сессия (myId, authKey, user, genCount, roots, isLogin); getters: getFio, getPhoto, getGptRoot, getSignature; logOut.
- **styleMode** — darkMode.
- **viewsData** — кэш лендингов (home, ourPeople, news, gallery, calendar...); setData/getData.
- **blogData** — блоги и авторы. **factoryGuid** — заводы/отчёты/туры. **pointsData** — активности.
- **referencesAndExpData** — референсы по заводам. **userScoreData** — баллы пользователя, история покупок.
- **adminData** — секции админки. **pageData** — текущий маршрут (подсветка меню).

### 4.4. API-слой (`utils/Api.ts`)
- Два Axios-инстанса: `api` (baseURL `VITE_API_URL`, withCredentials) и `vendorApi` (gpt.emk.ru).
- **Авторизация**: cookie `session_id` (HttpOnly) + заголовок `session_id`, добавляемый interceptor'ом из `userData.authKey`.
- 502 → редирект на `/inservice`; 401 → `logOut()`.
- Основные эндпоинты: `article/find_by/{sectionId}`, `article/find_by_ID/{id}`, `b24/calendar/{from}/{to}`, `/peer/*`.

### 4.5. Ключевые компоненты
- **Layout**: Header (многоуровневое меню с visibility), ModeChanger (день/ночь), RightSidebar (календарь, соцсети), TopRightSidebar (ЛК), Breadcrumbs, LayoutPostsPreview, Loader, SnowFlakes, SinerTable.
- **Gallery**: SampleGallery, ComplexGallery (+ ZoomModal).
- **Swiper**: SwiperBlank (видео/изображения), FullWidthSlider, SwiperButtons.
- **Modal**: ZoomModal, SlotModal, PdfViewerModal, SearchModal (глобальный поиск).
- **tools/common**: PostInner, Reactions (лайки), VerticalCard, TextEditor (Quill), FileUploader, SearchList, DatePicker, PageSelector, CustomFilter/DateFilter/TagsFilter, YandexMetrika.

### 4.6. Utils и статика
- **composables**: usePrefetchSection (центральный загрузчик по секциям, маппинг sectionTips), useBlogAuthors, useExperienceData, useFile, useSwiperConf, useToast.
- **utils**: Api, apiResponseCheck, dateConvert, parseMarkdown, sanitizeHtml, embedVideoUtil, screenCheck, createMail, calendarTypeFormat, stringUtils. Юнит-тесты Vitest в `specs/`.
- **assets/static**: `sectionTips.ts` (название секции → id B24), `navLinks.ts`, `featureFlags.ts`, `adminSections.ts`, `trainingCenterData.ts`, `safetyTechnics.ts`, `factoryLogoTips.ts`, `testMode.ts`.

### 4.7. Стили (SCSS)
- `_main.scss` — точка входа (@forward partials). `_vars.scss` — CSS-переменные (`--emk-brand-color: #f5821f`).
- Брейкпоинты `_mixins.scss`: xxl 1400 / xl 1400 / lg 1200 / md 992 / sm 768.
- Тёмная тема — партиал `layout/_darkMode.scss` (переопределения под `.dark-mode`), не CSS-переменные.

### 4.8. Views (назначение разделов)
- **home** — главная (swiper/section блоки, автообновление 240 c).
- **about** — компания, книга истории (главы), наши люди, итоги года, блоги, учебный центр, памятка новичка, дни рождения, ТБ, вакансии, календарь, «о капитале», магазин мерча.
- **news** — актуальные/корпоративные новости, синертим, газета.
- **gallery** — гид по предприятиям (3D-туры), официальные события, видеосекции, фильмы.
- **innerCommunications** — корпсобытия, корпжизнь, афиша, партнёры, благотворительность, конкурсы.
- **services** — открытки, нейрочат (GPT), референсы/опыт поставок.
- **user** — личный кабинет, банк идей, балльная система.
- **admin** — редактор контента, балльная система (суперадмин/модератор/куратор), права, области видимости.
- **vcard** — электронная визитка (отдельный layout).

---

## 5. Интерфейсы и типы (front/src/interfaces)
- **IEntities.ts** — barrel, реэкспортирует сущности.
- **IBase.ts** — базовые: `IReaction` (views+likes), `IBXFileType`, `IBaseEntity` (id, name, content, reactions, tags, images, documentation, videos, preview_file_url...), `IBaseIndirectData` (поля B24).
- **IUser.ts**, **INews.ts**, **IBlogs.ts**, **ICalendar.ts**, **IFactoryGuid.ts**, **IReferencsExp.ts**,
  **IAdminPoints.ts** (баллы), **IAdmin.ts** (roots, редактирование), **ITable.ts**, **IMerch.ts**, **IIdea.ts**,
  **IMainPage.ts**, **ILayout.ts**, **IKrpano.ts** (3D-туры), **IPostFetch.ts**, **IPutFetchData.ts**.

---

## 6. Сборка (Dockerfile)
- **code/Dockerfile**: `python:3.13-slim`, LibreOffice (для docx→pdf), pip-зеркало aliyun, `CMD python3 run.py` (uvicorn 0.0.0.0:8000).
- **front/Dockerfile**: многоступенчатая, node:22-alpine, npm install + build, `CMD npm run preview` (vite preview, порт 5173).

---

## 7. Известные проблемы и риски
1. В `B24.py` и `Auth.py` захардкожены webhook-токены, client_id/secret, пароли — секреты в коде.
2. `test.py` содержит реальные REST-запросы с `session_id` и API-ключом B24.
3. Kibana-пароль `MyPw123` рассинхронизирован с `ELASTIC_PASSWORD=${pswd}`; kibana-сервис не в compose.
4. `elasticsearch.yml` и `kibana/config.yml` фактически НЕ монтируются в compose.
5. Promtail собирает логи только `fastapi_async`.
6. `AdminPanel.py`: вызов `Auth()` вместо `AuthService()`, перезапуск firewall закомментирован.
7. `code/__init__.py`: в `__all__` местами пропущены запятые (конкатенация строк).
8. Дублирование зависимостей авторизации `get_user_id_by_session_id`/`get_current_user` в разных файлах.
9. `AIchat.get_current_user` содержит неопределённую переменную `auth_header` (баг).
10. Старый/устаревший код ссылается на несуществующие поля (created_at, subscription_status и т.д.).
11. `front/Dockerfile` использует `npm install` (не `npm ci`) и `vite preview` вместо production-сервера.
12. MongoDB (порт 27017) упоминается в firewall/env, но сервиса нет в compose.