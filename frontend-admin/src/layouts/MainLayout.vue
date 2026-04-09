<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="240px" class="sidebar">
      <div class="logo">
        <el-icon size="28"><Setting /></el-icon>
        <span>QDPS</span>
      </div>
      <el-menu
        :default-active="$route.path"
        background-color="#0a2647"
        text-color="#94a3b8"
        active-text-color="#57c5b6"
        router
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>系统首页</span>
        </el-menu-item>
        
        <el-sub-menu index="dimension">
          <template #title>
            <el-icon><DataLine /></el-icon>
            <span>尺寸判定</span>
          </template>
          <el-menu-item index="/dimension/three">三动全尺寸判定</el-menu-item>
          <el-menu-item index="/dimension/four">四动全尺寸判定</el-menu-item>
          <el-menu-item index="/dimension/five">五动全尺寸判定</el-menu-item>
        </el-sub-menu>
        
        <el-menu-item index="/certificate">
          <el-icon><Document /></el-icon>
          <span>质量证明单号</span>
        </el-menu-item>
        
        <el-sub-menu index="maintenance">
          <template #title>
            <el-icon><Tools /></el-icon>
            <span>基础数据维护</span>
          </template>
          <el-menu-item index="/maintenance/product-quality">产品检测数据维护</el-menu-item>
          <el-menu-item index="/maintenance/report-path">报告路径维护</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    
    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航 -->
      <el-header class="header">
        <div class="header-title">{{ pageTitle }}</div>
        <div class="header-user">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
              <div class="user-avatar">
                {{ userStore.user?.display_name?.charAt(0) || 'U' }}
              </div>
              <div class="user-detail">
                <span class="user-name">{{ userStore.user?.display_name }}</span>
                <span class="user-dept">{{ userStore.user?.department || '质量部' }}</span>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item disabled>
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ userStore.user?.department || '质量部' }}
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 内容区 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const pageTitle = computed(() => {
  const titles = {
    '/': '系统首页',
    '/dimension/three': '三动全尺寸判定',
    '/dimension/four': '四动全尺寸判定',
    '/dimension/five': '五动全尺寸判定',
    '/certificate': '质量证明单号',
    '/maintenance/product-quality': '产品检测数据维护',
    '/maintenance/report-path': '报告路径维护'
  }
  return titles[route.path] || 'QDPS'
})

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      router.push('/login')
    }).catch(() => {})
  }
}
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background: linear-gradient(180deg, #0a2647 0%, #1a5f7a 100%);
  overflow-y: auto;
  
  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    .el-icon {
      color: #57c5b6;
    }
  }
  
  :deep(.el-menu) {
    border: none;
  }
  
  :deep(.el-menu-item:hover),
  :deep(.el-sub-menu__title:hover) {
    background-color: rgba(255, 255, 255, 0.1) !important;
  }
  
  :deep(.el-menu-item.is-active) {
    background-color: rgba(87, 197, 182, 0.2) !important;
    border-left: 3px solid #57c5b6;
  }
}

.header {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  
  .header-title {
    font-size: 18px;
    font-weight: 600;
    color: #0a2647;
  }
  
  .header-user {
    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 6px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:hover {
        background: #f5f7fa;
      }
      
      .user-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #57c5b6 0%, #1a5f7a 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(87, 197, 182, 0.4);
      }
      
      .user-detail {
        display: flex;
        flex-direction: column;
        gap: 2px;
        
        .user-name {
          font-weight: 600;
          color: #303133;
          font-size: 14px;
          line-height: 1.2;
        }
        
        .user-dept {
          color: #909399;
          font-size: 12px;
          line-height: 1.2;
        }
      }
      
      .dropdown-icon {
        color: #909399;
        font-size: 12px;
        transition: transform 0.3s;
      }
    }
    
    :deep(.el-dropdown-menu__item) {
      padding: 8px 16px;
      
      .el-icon {
        margin-right: 8px;
        color: #909399;
      }
    }
  }
}

.main-content {
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>
