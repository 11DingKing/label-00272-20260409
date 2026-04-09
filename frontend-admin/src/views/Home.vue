<template>
  <div class="home-page">
    <!-- 欢迎卡片 -->
    <div class="welcome-card">
      <div class="welcome-content">
        <h2>欢迎使用 QDPS 质量数据处理系统</h2>
        <p>
          您好，{{ userStore.user?.display_name }}！今天是 {{ currentDate }}
        </p>
      </div>
      <el-icon size="80" color="rgba(255,255,255,0.2)"><TrendCharts /></el-icon>
    </div>

    <!-- 功能卡片 -->
    <el-row :gutter="20">
      <el-col :span="8" v-for="item in modules" :key="item.path">
        <div 
          class="feature-card" 
          :class="{ 'feature-card-disabled': !item.enabled }"
          @click="handleCardClick(item)"
        >
          <div class="card-content">
            <div class="feature-icon" :style="{ background: item.gradient }">
              <el-icon size="28"><component :is="item.icon" /></el-icon>
            </div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
          </div>
          <el-button text type="primary" class="enter-button" :disabled="!item.enabled">
            进入功能 <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import api from "@/utils/api";
import { ElMessage } from "element-plus";

const userStore = useUserStore();
const router = useRouter();
const modules = ref([]);

const currentDate = computed(() => {
  return new Date().toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
  });
});

const handleCardClick = (item) => {
  if (item.enabled) {
    router.push(item.path);
  } else {
    ElMessage.warning("该功能模块已禁用");
  }
};

const fetchModules = async () => {
  try {
    const res = await api.get("/api/modules");
    if (res.success) {
      modules.value = res.data;
    }
  } catch (error) {
    console.error("获取模块列表失败:", error);
  }
};

onMounted(() => {
  fetchModules();
});
</script>

<style lang="scss" scoped>
.welcome-card {
  background: linear-gradient(135deg, #1a5f7a, #159895);
  border-radius: 12px;
  padding: 32px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  h2 {
    font-size: 22px;
    margin: 0 0 8px;
  }
  p {
    margin: 0;
    opacity: 0.9;
  }
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  height: 240px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);

    .enter-button {
      color: #159895;
    }
  }

  .card-content {
    flex: 1;
  }

  .feature-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-bottom: 16px;
  }

  h3 {
    font-size: 16px;
    color: #303133;
    margin: 0 0 8px;
    font-weight: 600;
  }

  p {
    font-size: 13px;
    color: #909399;
    margin: 0;
    line-height: 1.6;
    min-height: 42px;
  }

  .enter-button {
    margin-top: 16px;
    padding: 0;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s;

    .el-icon {
      margin-left: 4px;
      transition: transform 0.3s;
    }

    &:hover .el-icon {
      transform: translateX(4px);
    }
  }
}

.feature-card-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  filter: grayscale(100%);

  &:hover {
    transform: none;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);

    .enter-button {
      color: #409eff;
    }
  }
}
</style>
