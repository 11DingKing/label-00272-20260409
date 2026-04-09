import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/utils/api'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: 'dimension/three',
        name: 'ThreeMotion',
        component: () => import('@/views/dimension/MotionCheck.vue'),
        props: { motionType: '三动' }
      },
      {
        path: 'dimension/four',
        name: 'FourMotion',
        component: () => import('@/views/dimension/MotionCheck.vue'),
        props: { motionType: '四动' }
      },
      {
        path: 'dimension/five',
        name: 'FiveMotion',
        component: () => import('@/views/dimension/MotionCheck.vue'),
        props: { motionType: '五动' }
      },
      {
        path: 'certificate',
        name: 'CertificateList',
        component: () => import('@/views/certificate/List.vue')
      },
      {
        path: 'certificate/create',
        name: 'CertificateCreate',
        component: () => import('@/views/certificate/Form.vue')
      },
      {
        path: 'certificate/edit/:id',
        name: 'CertificateEdit',
        component: () => import('@/views/certificate/Form.vue')
      },
      {
        path: 'certificate/view/:id',
        name: 'CertificateView',
        component: () => import('@/views/certificate/View.vue')
      },
      {
        path: 'maintenance/product-quality',
        name: 'ProductQuality',
        component: () => import('@/views/maintenance/ProductQuality.vue')
      },
      {
        path: 'maintenance/report-path',
        name: 'ReportPath',
        component: () => import('@/views/maintenance/ReportPath.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 不需要认证的页面直接放行
  if (to.meta.requiresAuth === false) {
    if (to.path === '/login' && userStore.isLoggedIn) {
      next('/')
    } else {
      next()
    }
    return
  }
  
  // 需要认证的页面，先检查本地是否有token
  if (!userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 有token，验证是否过期
  try {
    await api.get('/api/auth/verify')
    next()
  } catch (error) {
    // token过期或无效，清除并跳转登录
    userStore.logout()
    next('/login')
  }
})

export default router
