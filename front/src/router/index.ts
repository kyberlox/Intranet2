import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'router-link-active',
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/about',
      name: 'personal',
      component: () => import('../views/about/ourCompany/OurCompany.vue')
    },
    {
      path: '/about/company-history',
      name: 'book-emk',
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
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/about/year-results',
      name: 'year-results',
      component: () => import('@/views/about/yearResults/YearResults.vue'),
    },
    {
      path: '/about/year-results/:id',
      name: 'year-results-id',
      component: () => import('@/views/about/yearResults/YearResults.vue'),
      props: (route) => ({ id: route.params.id })
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
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/about/blogs/:authorId/:id',
      name: 'CertainBlog',
      component: () => import('@/views/about/blogs/CertainBlog.vue'),
      props: (route) => ({ authorId: route.params.authorId, id: route.params.id })
    },
    {
      path: '/about/videoInterviews',
      name: 'videoInterviews',
      component: () => import('@/views/about/videoInterview/VideoInterviews.vue'),
    },
    {
      path: '/about/videoInterviews/:id',
      name: 'videoInterview',
      component: () => import('@/views/about/videoInterview/VideoInterviewInner.vue'),
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/about/videoreports',
      name: 'videoreports',
      component: () => import('@/views/news/videoReports/VideoReports.vue'),
    },
    {
      path: '/about/videoreports/:id',
      name: 'videoreport',
      component: () => import('@/views/news/videoReports/VideoReports.vue'),
      props: (route) => ({ id: route.params.id })
    },
    {
      path: '/about/trainingcenter',
      name: 'training',
      component: () => import('@/views/about/trainingCenter/TrainingCenter.vue')
    },
    {
      path: '/about/trainingcenter/ecources',
      name: 'Ecources',
      component: () => import('@/views/about/trainingCenter/ecources/Ecources.vue')
    },
    {
      path: '/about/trainingcenter/ecources/:id',
      name: 'Ecource',
      component: () => import('@/views/about/trainingCenter/ecources/CourceDescription.vue')
    },
    {
      path: '/about/trainingcenter/trainings',
      name: 'conductedTrainings',
      component: () => import('@/views/about/trainingCenter/conductedTrainings/СonductedTrainingsInner.vue'),
    },
    {
      path: '/about/trainingcenter/trainings/:id',
      name: 'conductedTraining',
      component: () => import('@/views/about/trainingCenter/conductedTrainings/Training.vue'),
    },
    {
      path: '/about/trainingcenter/announces',
      name: 'trainingAnnounces',
      component: () => import('@/views/about/trainingCenter/announces/TrainingAnnounces.vue')
    },
    {
      path: '/about/trainingcenter/excursions',
      name: 'excursions',
      component: () => import('@/views/about/trainingCenter/excursions/Excursions.vue')
    },
    {
      path: '/about/trainingcenter/literature',
      name: 'literature',
      component: () => import('@/views/about/trainingCenter/literature/Literature.vue')
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
      name: 'fornewworker',
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
      component: () => import('@/views/about/safetyTechnics/SafetyTechnicsCovid.vue')
    },
    {
      path: '/about/safetytechnics/fire',
      name: 'safetytechnicsFire',
      component: () => import('@/views/about/safetyTechnics/SafetyTechnicsFire.vue')
    },
    {
      path: '/about/safetytechnics/factory',
      name: 'safetytechnicsFactory',
      component: () => import('@/views/about/safetyTechnics/SafetyTechnicsFactory.vue')
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
      path: '/services/selectionTep',
      name: 'selectionTep',
      beforeEnter: (to, from, next) => {
        window.open('https://emk.websto.pro/static/select.html', '_blank')
        next(false)
      },
      redirect: '',
    },
    {
      path: '/services/selectionReg',
      name: 'selectionReg',
      beforeEnter: (to, from, next) => {
        window.open('https://portal.emk.ru/intranet/tools/regconf.php', '_blank')
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
      component: () => import('@/views/services/ChatGpt.vue')
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
      path: '/services/experience/:title',
      name: 'experienceTypes',
      component: () => import('@/views/services/experience/ExperienceTypes.vue')
    },
    {
      path: '/services/experience/:title/:id',
      name: 'experienceType',
      component: () => import('@/views/services/experience/ExperienceType.vue')
    },
    {
      path: '/news/actual',
      name: 'actualNews',
      component: () => import('@/views/news/actualNews/ActualNews.vue')
    },
    {
      path: '/news/actual/:id',
      name: 'actualArticle',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Актуальные новости' })
    },
    {
      path: '/news/corpnews',
      name: 'corpnews',
      component: () => import('@/views/news/corpNews/CorpNews.vue')
    },
    {
      path: '/news/corpnews/:id',
      name: 'corpNewsArticle',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Новости организационного развития' })
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
      path: '/gallery/factories/reports/:title',
      name: 'factoriesReports',
      component: () => import('@/views/gallery/factoryGuid/FactoryReports.vue')
    },
    {
      path: '/gallery/factories/tours/:title',
      name: 'factoriesTours',
      component: () => import('@/views/gallery/factoryGuid/FactoryTours.vue')
    },
    {
      path: '/gallery/factories/tours/:title/:id',
      name: 'factoryTour',
      component: () => import('@/views/gallery/factoryGuid/FactoryTour.vue')
    },
    {
      path: '/communications/officialevents',
      name: 'officialEvents',
      component: () => import('@/views/gallery/officialEvents/OfficialEvents.vue')
    },
    {
      path: '/communications/officialevents/:id',
      name: 'officialEvent',
      component: () => import('@/views/gallery/officialEvents/OfficialEvent.vue')
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
      props: (route) => ({ id: route.params.id, pageTitle: 'Корпоративные события' })
    },
    {
      path: '/communications/corplife/',
      name: 'corpLife',
      component: () => import('@/views/innerCommunications/CorpLife.vue')
    },
    {
      path: '/communications/corplife/:id',
      name: 'corpLifeItem',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Корпоративная жизнь', type: 'onlyImg' })
    },
    {
      path: '/communications/announces/',
      name: 'eventAnnounces',
      component: () => import('@/views/innerCommunications/EventAnnounces.vue')
    },
    {
      path: '/communications/announces/:id',
      name: 'eventAnnounce',
      component: () => import('@/views/PostPreview.vue'),
      props: (route) => ({ id: route.params.id, pageTitle: 'Афиша' })
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
      props: (route) => ({ id: route.params.id, pageTitle: 'Предложения партнеров' })
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
      props: (route) => ({ id: route.params.id, pageTitle: 'Благотворительные проекты' })
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
      path: '/user/ideas',
      name: 'ideasPage',
      component: () => import('@/views/user/MyIdeas.vue')
    },
    {
      path: '/user/ideas/new',
      name: 'newIdeaPage',
      component: () => import('@/views/user/NewIdea.vue')
    }
  ]
})

export default router