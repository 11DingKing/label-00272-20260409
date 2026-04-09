import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 30000
})

// 防止重复跳转
let isRedirecting = false

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 保存当前路由，登录后跳转
      const currentPath = router.currentRoute.value.fullPath
      if (currentPath !== '/login') {
        localStorage.setItem('redirectPath', currentPath)
      }
      if (!isRedirecting) {
        isRedirecting = true
        router.push('/login').finally(() => {
          isRedirecting = false
        })
      }
    } else {
      ElMessage.error(error.response?.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default api
