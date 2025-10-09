import { createRouter, createWebHistory } from 'vue-router'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'router-link-active',
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/homeView/HomeView.vue'),
    },
    {
      path: '/about',
      name: 'personal',
      component: () => import('../views/about/ourCompany/OurCompany.vue'),
    },
    {
      path: '/about/company-history',
      name: 'book-emk',
      component: () => import('../views/about/companyHistory/CompanyHistory.vue'),
    },
    {
      path: '/about/company-history/:id',
      name: 'book-emk-page',
      component: () => import('../views/about/companyHistory/CompanyHistory.vue'),
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/about/our-people',
      name: 'our-people',
      component: () => import('@/views/about/ourPeople/OurPeople.vue'),
    },
    {
      path: '/about/our-people/:id',
      name: 'ourPeopleInner',
      component: () => import('@/views/about/ourPeople/OurPeopleInner.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Наши люди', route: 'our-people' }]
      }
    },
    {
    path: '/about/year-results/:id?', 
    name: 'year-results',
    component: () => import('@/views/about/yearResults/YearResults.vue'),
    props: (route) => ({ id: route.params.id || null }),
    },
    {
      path: '/about/blogs',
      name: 'blogs',
      component: () => import('@/views/about/blogs/Blogs.vue'),
    },
    {
      path: '/about/blogs/:id',
      name: 'blogOf',
      component: () => import('@/views/about/blogs/BlogsAritcles.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Блоги', route: 'blogs' }]
      }
    },
    {
      path: '/about/blogs/:authorId/:id',
      name: 'certainBlog',
      component: () => import('@/views/about/blogs/CertainBlog.vue'),
      props: (route) => ({ authorId: route.params.authorId, id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Блоги', route: 'blogs' }]
      }
    },
    {
      path: '/about/videoInterviews',
      name: 'videoInterviews',
      component: () => import('@/views/about/videoInterview/VideoInterviews.vue'),
    },
    {
      path: '/about/videoInterviews/:id',
      name: 'videoInterview',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Видеоинтервью' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Видеоинтервью', route: 'videoInterviews' }]
      }
    },
    {
      path: '/about/videoreports',
      name: 'videoReports',
      component: () => import('@/views/news/videoReports/VideoReports.vue'),
    },
    {
      path: '/about/videoreportsByTag/:tagId',
      name: 'videoReportsByTag',
      props: (route) => ({ tagId: route.params.tagId}),
      component: () => import('@/views/news/videoReports/VideoReports.vue'),
    },
    {
      path: '/about/videoreports/:id',
      name: 'videoReport',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Видеорепортажи' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Видеорепортажи', route: 'videoReports' }]
      }
    },
    {
      path: '/about/trainingcenter',
      name: 'trainingcenter',
      component: () => import('@/views/about/trainingCenter/TrainingCenter.vue')
    },
    {
      path: '/about/trainingcenter/ecources',
      name: 'Ecources',
      component: () => import('@/views/about/trainingCenter/ecources/Ecources.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }]
      }
    },
    {
      path: '/about/trainingcenter/ecources/:id',
      name: 'Ecource',
      component: () => import('@/views/about/trainingCenter/ecources/CourceDescription.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }, { title: 'Курсы', route: 'Ecources' }]
      }
    },
    {
      path: '/about/trainingcenter/trainings',
      name: 'conductedTrainings',
      component: () => import('@/views/about/trainingCenter/conductedTrainings/СonductedTrainings.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }]
      }
    },
    {
      path: '/about/trainingcenter/trainings/:id',
      name: 'conductedTraining',
      component: () => import('@/views/about/trainingCenter/conductedTrainings/FeedBackModalInner.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }, { title: 'Тренинги', route: 'conductedTrainings' }]
      }
    },
    {
      path: '/about/trainingcenter/announces',
      name: 'trainingAnnounces',
      component: () => import('@/views/about/trainingCenter/announces/TrainingAnnounces.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }]
      }
    },
    {
      path: '/about/trainingcenter/excursions',
      name: 'excursions',
      component: () => import('@/views/PostPreview.vue'),
      props: () => ({ pageTitle: 'Экскурсии' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }]
      }
    },
    {
      path: '/about/trainingcenter/literature',
      name: 'literature',
      component: () => import('@/views/about/trainingCenter/literature/Literature.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Учебный центр', route: 'trainingcenter' }]
      }
    },
    {
      path: '/about/trainingcenter/memo1c',
      name: 'memo1c',
      beforeEnter: (to, from, next) => {
        window.open('http://1c-help.websto.pro/', '_blank')
        next(false)
      },
      redirect: '',
    },
    {
      path: '/about/fornewworker',
      name: 'forNewWorker',
      component: () => import('@/views/about/forNewWorker/ForNewWorker.vue')
    },
    {
      path: '/about/birthdays',
      name: 'birthdays',
      component: () => import('@/views/about/birthdays/Birthdays.vue')
    },
    {
      path: '/about/safetytechnics',
      name: 'safetytechnics',
      component: () => import('@/views/about/safetyTechnics/SafetyTechnics.vue')
    },
    {
      path: '/about/safetytechnics/covid',
      name: 'safetytechnicsCovid',
      component: () => import('@/views/about/safetyTechnics/SafetyTechnicsCovid.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Техника безопасности', route: 'safetytechnics' }]
      }
    },
    {
      path: '/about/safetytechnics/fire',
      name: 'safetytechnicsFire',
      component: () => import('@/views/about/safetyTechnics/SafetyTechnicsFire.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Техника безопасности', route: 'safetytechnics' }]
      }
    },
    {
      path: '/about/safetytechnics/factory',
      name: 'safetytechnicsFactory',
      component: () => import('@/views/about/safetyTechnics/SafetyTechnicsFactory.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Техника безопасности', route: 'safetytechnics' }]
      }
    },
    {
      path: '/about/vacancies',
      name: 'vacancies',
      component: () => import('@/views/about/referFriend/ReferFriend.vue')
    },
    {
      path: '/about/newworkers',
      name: 'newWorkers',
      component: () => import('@/views/about/newWorkers/NewWorkers.vue')
    },
    {
      path: '/about/calendar',
      name: 'calendar',
      component: () => import('@/views/about/calendarPage/CalendarPage.vue')
    },
    {
      path: '/about/calendar/:targetId',
      name: 'calendarMonth',
      component: () => import('@/views/about/calendarPage/CalendarPage.vue'),
      props: (route) => ({ targetId: route.params.targetId }),
    },
    {
      path: '/about/merch',
      name: 'merchStore',
      component: () => import('@/views/about/merchStore/MerchStore.vue'),
    },
    {
      path: '/about/merch/:id',
      name: 'merchStoreItem',
      component: () => import('@/views/about/merchStore/MerchStoreItem.vue'),
      props: (route) => ({ id: Number(route.params.id) }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Магазин мерча', route: 'merchStore' }]
      }
    },
    {
      path: '/services/selectionTep',
      name: 'selectionTep',
      beforeEnter: (to, from, next) => {
        window.open('https://tepconf.emk.ru', '_blank')
        next(false)
      },
      redirect: '',
    },
    {
      path: '/services/selectionReg',
      name: 'selectionReg',
      beforeEnter: (to, from, next) => {
        window.open('https://regconf.emk.ru', '_blank')
        next(false)
      },
      redirect: '',
    },
    {
      path: '/services/postcard',
      name: 'postcard',
      component: () => import('@/views/services/PostCard.vue')
    },
    {
      path: '/services/chatgpt',
      name: 'chatgpt',
      component: () => import('@/views/services/chatGpt/NeuroChat.vue')
    },
    {
      path: '/services/cert',
      name: 'cert',
      beforeEnter: (to, from, next) => {
        window.open('http://cert.imp.int/', '_blank')
        next(false)
      },
      redirect: '',
    },
    {
      path: '/services/experience',
      name: 'experience',
      component: () => import('@/views/services/experience/Experience.vue')
    },
    {
      path: '/services/experience/:factoryId',
      name: 'experienceTypes',
      component: () => import('@/views/services/experience/ExperienceTypes.vue'),
      props: (route) => ({ factoryId: route.params.factoryId }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Референсы', route: 'experience' }]
      }
    },
    {
      path: '/services/experience/:factoryId/:sectorId',
      name: 'experienceType',
      component: () => import('@/views/services/experience/ExperienceType.vue'),
      props: (route) => ({ factoryId: route.params.factoryId, sectorId: route.params.sectorId }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Референсы', route: 'experience' }]
      }
    },
    {
      path: '/news/actual',
      name: 'actualNews',
      component: () => import('@/views/news/actualNews/ActualNews.vue')
    },
    {
      path: '/news/actual/tag/:tagId',
      name: 'actualNewsByTag',
      props: (route) => ({ tagId: route.params.tagId}),
      component: () => import('@/views/news/actualNews/ActualNews.vue')
    },
    {
      path: '/news/actual/:id',
      name: 'actualArticle',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Актуальные новости' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Актуальные новости', route: 'actualNews' }]
      }
    },
    {
      path: '/news/corpnews',
      name: 'corpNews',
      component: () => import('@/views/news/corpNews/CorpNews.vue')
    },
    {
      path: '/news/corpnews/:id',
      name: 'corpNewsArticle',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Новости организационного развития' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Новости организационного развития', route: 'corpNews' }]
      }
    },
    {
      path: '/news/gazette',
      name: 'gazette',
      component: () => import('@/views/news/gazette/Gazette.vue')
    },
    {
      path: '/gallery/factories',
      name: 'factories',
      component: () => import('@/views/gallery/factoryGuid/Factories.vue')
    },
    {
      path: '/gallery/factories/reports/:id',
      name: 'factoryReports',
      component: () => import('@/views/gallery/factoryGuid/FactoryReports.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Гид по предприятиям', route: 'factories' }]
      }
    },
    {
      path: '/gallery/factories/tours/:id',
      name: 'factoryTours',
      component: () => import('@/views/gallery/factoryGuid/FactoryTours.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Гид по предприятиям', route: 'factories' }]
      }
    },
    {
      path: '/gallery/factories/tours/:id/:tourId',
      name: 'factoryTour',
      component: () => import('@/views/gallery/factoryGuid/FactoryTour.vue'),
      props: (route) => ({ id: route.params.tourId, factoryId: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Гид по предприятиям', route: 'factories' }]
      }
    },
    {
      path: '/communications/officialevents',
      name: 'officialEvents',
      component: () => import('@/views/gallery/officialEvents/OfficialEvents.vue')
    },
    {
      path: '/communications/officialevents/:id',
      name: 'officialEvent',
      component: () => import('@/views/gallery/officialEvents/OfficialEvent.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Официальные события', route: 'officialEvents' }]
      }
    },
    {
      path: '/communications/corpevents/',
      name: 'corpEvents',
      component: () => import('@/views/innerCommunications/CorpEvents.vue'),
    },
    {
      path: '/communications/corpevent/:id',
      name: 'corpEvent',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Корпоративные события' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Корпоративные события', route: 'corpEvents' }]
      }
    },
    {
      path: '/communications/corplife/',
      name: 'corpLife',
      component: () => import('@/views/innerCommunications/corpLife/CorpLife.vue')
    },
    {
      path: '/communications/corplife/:id',
      name: 'corpLifeItem',
      component: () => import('@/views/innerCommunications/corpLife/CorpLifeItem.vue'),
      props: (route) => ({ id: route.params.id }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Корпоративная жизнь', route: 'corpLife' }]
      }
    },
    {
      path: '/communications/announces/',
      name: 'eventAnnounces',
      component: () => import('@/views/innerCommunications/EventAnnounces.vue')
    },
    {
      path: '/communications/contest/',
      name: 'contest',
      component: () => import('@/views/innerCommunications/ContestEmk.vue')
    },
    {
      path: '/communications/announces/:id',
      name: 'eventAnnounce',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Афиша' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Афиша', route: 'eventAnnounces' }]
      }
    },
    {
      path: '/gallery/partners/',
      name: 'partners',
      component: () => import('@/views/innerCommunications/PartnerBonus.vue'),
    },
    {
      path: '/gallery/partners/:id',
      name: 'partnerPost',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Предложения партнеров' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Предложения партнеров', route: 'partners' }]
      }
    },
    {
      path: '/gallery/care/',
      name: 'care',
      component: () => import('@/views/innerCommunications/Care.vue')
    },
    {
      path: '/gallery/care/:id',
      name: 'carePost',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Благотворительные проекты' }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Благотворительные проекты', route: 'care' }]
      }
    },
    {
      path: '/user/auth',
      name: 'auth',
      component: () => import('@/views/user/AuthPage.vue')
    },
    {
      path: '/user/:id',
      name: 'userPage',
      component: () => import('@/views/user/UserPage.vue'),
      props: (route) => ({ id: route.params.id })

    },
    {
      path: '/user/ideas/',
      name: 'ideasPage',
      component: () => import('@/views/user/ideas/MyIdeas.vue'),
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/user/ideas/new',
      name: 'newIdeaPage',
      component: () => import('@/views/user/ideas/NewIdea.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/admin/components/AdminSidebar.vue')
    },
    {
      path: '/admin/:id',
      name: 'adminBlockInner',
      component: () => import('@/views/admin/editPanel/AdminElements.vue'),
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/admin/:id/new',
      name: 'adminElementInnerAdd',
      component: () => import('@/views/admin/editPanel/AdminElementInner.vue'),
      props: (route) => ({ id: route.params.id, type: 'new' }),
    },
    {
      path: '/admin/:id/:elementId',
      name: 'adminElementInnerEdit',
      component: () => import('@/views/admin/editPanel/AdminElementInner.vue'),
      props: (route) => ({ id: route.params.id, elementId: route.params.elementId }),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Список редактора', route: 'adminBlockInner' }]
      }
    },
    {
      path: '/admin/visibility',
      name: 'visibilityArea',
      component: () => import('@/views/admin/visibilityAreaEditor/VisibilityAreaEditor.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Список редактора', route: 'admin' }]
      }
    },
    {
      path: '/admin/files',
      name: 'fileManager',
      component: () => import('@/views/admin/visibilityAreaEditor/VisibilityAreaEditor.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Список редактора', route: 'admin' }]
      }
    },
    {
      path: '/admin/scoreAdmin',
      name: 'pointsAdministrator',
      component: () => import('@/views/admin/pointsSystem/superAdminPanel/SuperAdminPanel.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Список редактора', route: 'admin' }]
      }
    },
    {
      path: '/admin/pointsmoderation',
      name: 'pointsModeration',
      component: () => import('@/views/admin/pointsSystem/moderatorPanel/ModeratorValidationPanel.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Список редактора', route: 'admin' }]
      }
    },
    {
      path: '/admin/curatorhistory',
      name: 'curatorHistory',
      component: () => import('@/views/admin/pointsSystem/curatorHistory/CuratorHistory.vue'),
      meta: {
        breadcrumbs: [{ title: 'Главная', route: 'home' }, { title: 'Список редактора', route: 'admin' }]
      }
    },
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' };
  }
})


export default router