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
        
        <!-- 尺寸判定子菜单 -->
        <el-sub-menu v-if="dimensionModules.length > 0" index="dimension">
          <template #title>
            <el-icon><DataLine /></el-icon>
            <span>尺寸判定</span>
          </template>
          <el-menu-item 
            v-for="item in dimensionModules" 
            :key="item.path" 
            :index="item.path"
            :disabled="!item.enabled"
          >
            {{ item.title }}
          </el-menu-item>
        </el-sub-menu>
        
        <!-- 质量证明单号 -->
        <el-menu-item 
          v-if="certificateModule" 
          :index="certificateModule.path"
          :disabled="!certificateModule.enabled"
        >
          <el-icon><Document /></el-icon>
          <span>{{ certificateModule.title }}</span>
        </el-menu-item>
        
        <!-- 基础数据维护子菜单 -->
        <el-sub-menu v-if="maintenanceModules.length > 0" index="maintenance">
          <template #title>
            <el-icon><Tools /></el-icon>
            <span>基础数据维护</span>
          </template>
          <el-menu-item 
            v-for="item in maintenanceModules" 
            :key="item.path" 
            :index="item.path"
            :disabled="!item.enabled"
          >
            {{ item.title }}
          </el-menu-item>
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
                {{ userStore.user?.display_name?.charAt(0) || "U" }}
              </div>
              <div class="user-detail">
                <span class="user-name">{{
                  userStore.user?.display_name
                }}</span>
                <span class="user-dept">{{
                  userStore.user?.department || "质量部"
                }}</span>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item disabled>
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ userStore.user?.department || "质量部" }}
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
    
    <!-- 操作日志悬浮按钮 -->
    <div class="log-float-button" @click="showLogPanel = true">
      <el-icon size="24"><Document /></el-icon>
    </div>
    
    <!-- 操作日志面板 -->
    <el-drawer
      v-model="showLogPanel"
      title="操作日志"
      direction="btt"
      :size="500"
      :modal-append-to-body="false"
      :append-to-body="true"
    >
      <div class="log-panel">
        <!-- 筛选区域 -->
        <div class="log-filter">
          <el-select 
            v-model="selectedModule" 
            placeholder="按模块筛选" 
            clearable
            style="width: 200px"
            @change="filterLogs"
          >
            <el-option 
              v-for="module in allModules" 
              :key="module.path" 
              :label="module.title" 
              :value="module.path"
            />
          </el-select>
          <el-button type="primary" @click="fetchLogs" style="margin-left: 12px">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
        
        <!-- 日志列表 -->
        <div class="log-list" v-loading="loadingLogs">
          <el-empty v-if="filteredLogs.length === 0" description="暂无操作日志" />
          <div v-else>
            <div 
              v-for="log in filteredLogs" 
              :key="log.id" 
              class="log-item"
            >
              <div class="log-header">
                <el-tag :type="getLogType(log.action)" size="small">
                  {{ log.action }}
                </el-tag>
                <span class="log-module">{{ getModuleTitle(log.module) }}</span>
                <span class="log-time">{{ formatTime(log.created_at) }}</span>
              </div>
              <div class="log-content">
                <span class="log-user">{{ log.user_name || '系统' }}：</span>
                <span class="log-message">{{ log.message }}</span>
              </div>
              <div v-if="log.details" class="log-details">
                <el-collapse>
                  <el-collapse-item title="查看详情">
                    <pre>{{ JSON.stringify(log.details, null, 2) }}</pre>
                  </el-collapse-item>
                </el-collapse>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-drawer>
  </el-container>
</template>

<script setup>
import { computed, ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { ElMessageBox } from "element-plus";
import api from "@/utils/api";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

// 模块列表
const allModules = ref([]);
const showLogPanel = ref(false);
const logs = ref([]);
const filteredLogs = ref([]);
const selectedModule = ref("");
const loadingLogs = ref(false);

// 按路径分组模块
const dimensionModules = computed(() => {
  return allModules.value.filter((m) => m.path.startsWith("/dimension/"));
});

const certificateModule = computed(() => {
  return allModules.value.find((m) => m.path === "/certificate");
});

const maintenanceModules = computed(() => {
  return allModules.value.filter((m) => m.path.startsWith("/maintenance/"));
});

const pageTitle = computed(() => {
  const titles = {
    "/": "系统首页",
    "/dimension/three": "三动全尺寸判定",
    "/dimension/four": "四动全尺寸判定",
    "/dimension/five": "五动全尺寸判定",
    "/certificate": "质量证明单号",
    "/maintenance/product-quality": "产品检测数据维护",
    "/maintenance/report-path": "报告路径维护",
  };
  return titles[route.path] || "QDPS";
});

const handleCommand = (command) => {
  if (command === "logout") {
    ElMessageBox.confirm("确定要退出登录吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(() => {
        userStore.logout();
        router.push("/login");
      })
      .catch(() => {});
  }
};

const fetchModules = async () => {
  try {
    const res = await api.get("/api/modules");
    if (res.success) {
      allModules.value = res.data;
    }
  } catch (error) {
    console.error("获取模块列表失败:", error);
  }
};

const fetchLogs = async () => {
  loadingLogs.value = true;
  try {
    const res = await api.get("/api/logs/recent");
    if (res.success) {
      logs.value = res.data;
      filterLogs();
    }
  } catch (error) {
    console.error("获取操作日志失败:", error);
  } finally {
    loadingLogs.value = false;
  }
};

const filterLogs = () => {
  if (!selectedModule.value) {
    filteredLogs.value = logs.value;
  } else {
    filteredLogs.value = logs.value.filter(
      (log) => log.module === selectedModule.value
    );
  }
};

const getModuleTitle = (modulePath) => {
  const module = allModules.value.find((m) => m.path === modulePath);
  return module ? module.title : modulePath;
};

const getLogType = (action) => {
  const typeMap = {
    创建: "success",
    修改: "warning",
    删除: "danger",
    查询: "info",
    登录: "primary",
    退出: "info",
  };
  return typeMap[action] || "info";
};

const formatTime = (time) => {
  if (!time) return "";
  const date = new Date(time);
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

// 监听日志面板显示，打开时获取日志
watch(showLogPanel, (val) => {
  if (val) {
    fetchLogs();
  }
});

onMounted(() => {
  fetchModules();
});
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
  position: relative;
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
  
  :deep(.el-menu-item.is-disabled) {
    opacity: 0.5;
    cursor: not-allowed;
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

// 悬浮按钮样式
.log-float-button {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #57c5b6 0%, #1a5f7a 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(87, 197, 182, 0.4);
  transition: all 0.3s ease;
  z-index: 999;
  
  &:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(87, 197, 182, 0.5);
  }
}

// 日志面板样式
.log-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.log-filter {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.log-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.log-item {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  
  &:hover {
    background: #eef1f6;
  }
}

.log-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 12px;
}

.log-module {
  color: #606266;
  font-size: 13px;
}

.log-time {
  color: #909399;
  font-size: 12px;
  margin-left: auto;
}

.log-content {
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
}

.log-user {
  font-weight: 500;
  color: #409eff;
}

.log-message {
  color: #606266;
}

.log-details {
  margin-top: 12px;
  
  :deep(.el-collapse) {
    border: none;
  }
  
  :deep(.el-collapse-item__header) {
    background: transparent;
    border: none;
    padding: 0;
    height: auto;
    line-height: 1.5;
    font-size: 12px;
    color: #909399;
  }
  
  :deep(.el-collapse-item__wrap) {
    border: none;
    background: transparent;
  }
  
  :deep(.el-collapse-item__content) {
    padding: 8px 0 0;
  }
  
  pre {
    background: #303133;
    color: #e5eaf3;
    padding: 12px;
    border-radius: 6px;
    font-size: 12px;
    overflow-x: auto;
    margin: 0;
  }
}

// 抽屉样式
:deep(.el-drawer) {
  .el-drawer__header {
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid #e4e7ed;
  }
  
  .el-drawer__body {
    padding: 0 20px 20px;
  }
}
</style>
