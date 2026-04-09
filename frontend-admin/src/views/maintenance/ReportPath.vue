<template>
  <div class="report-path-page">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><FolderOpened /></el-icon>
            <span class="header-title">报告存储路径配置</span>
          </div>
        </div>
      </template>
      
      <el-alert 
        type="info" 
        :closable="false" 
        class="info-alert"
        show-icon
      >
        <template #title>
          <span class="alert-title">配置说明</span>
        </template>
        配置系统生成的判定报告的存储位置。支持本地路径和网络UNC路径。
      </el-alert>
      
      <div class="form-container">
        <el-form label-width="160px" label-position="left" class="path-form">
          <el-form-item label="当前报告存储路径" class="current-path-item">
            <div class="current-path-display">
              <el-icon class="path-icon"><Folder /></el-icon>
              <span class="path-text">{{ currentPath || '未配置' }}</span>
              <el-tag v-if="currentPath" size="small" type="success" class="status-tag">已配置</el-tag>
              <el-tag v-else size="small" type="warning" class="status-tag">未配置</el-tag>
            </div>
          </el-form-item>
          
          <el-form-item label="新路径" required class="new-path-item">
            <div class="input-wrapper">
              <el-input 
                v-model="newPath" 
                placeholder="请输入新的报告存储路径" 
                size="large"
                clearable
                class="path-input"
              >
                <template #prefix>
                  <el-icon><FolderAdd /></el-icon>
                </template>
              </el-input>
            </div>
          </el-form-item>
          
          <el-form-item class="button-group">
            <div class="buttons-wrapper">
              <el-button 
                type="primary" 
                size="large"
                :loading="loading" 
                :icon="Check"
                @click="handleSave"
                class="save-button"
              >
                保存配置
              </el-button>
              <el-button 
                size="large"
                :icon="RefreshLeft"
                @click="handleReset"
                class="reset-button"
              >
                重置
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
      
      <el-divider />
      
      <div class="config-guide">
        <div class="guide-section">
          <div class="section-header">
            <el-icon class="section-icon"><Document /></el-icon>
            <h4>路径示例</h4>
          </div>
          <div class="examples-grid">
            <div class="example-item">
              <el-tag type="primary" size="small">Windows本地</el-tag>
              <code>D:\QDPS\报告</code>
            </div>
            <div class="example-item">
              <el-tag type="success" size="small">网络共享</el-tag>
              <code>\\192.168.1.100\share\报告</code>
            </div>
            <div class="example-item">
              <el-tag type="warning" size="small">Linux路径</el-tag>
              <code>/data/reports</code>
            </div>
          </div>
        </div>
        
        <div class="guide-section">
          <div class="section-header">
            <el-icon class="section-icon"><Warning /></el-icon>
            <h4>注意事项</h4>
          </div>
          <ul class="notice-list">
            <li>
              <el-icon class="list-icon"><Check /></el-icon>
              <span>确保系统对配置的路径具有读写权限</span>
            </li>
            <li>
              <el-icon class="list-icon"><Check /></el-icon>
              <span>如果使用网络路径，请确保网络连接稳定</span>
            </li>
            <li>
              <el-icon class="list-icon"><Check /></el-icon>
              <span>修改路径后，新生成的报告将保存到新路径</span>
            </li>
          </ul>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Check, RefreshLeft, CircleCheck, Warning } from '@element-plus/icons-vue'
import api from '@/utils/api'

const currentPath = ref('')
const newPath = ref('')
const loading = ref(false)

onMounted(async () => {
  try {
    const res = await api.get('/api/maintenance/report-path')
    if (res.success) {
      currentPath.value = res.data.path
    }
  } catch (error) {
    ElMessage.error('获取路径配置失败')
  }
})

const handleSave = async () => {
  if (!newPath.value.trim()) {
    ElMessage.warning('请输入新路径')
    return
  }
  
  loading.value = true
  try {
    const res = await api.put('/api/maintenance/report-path', { path: newPath.value })
    if (res.success) {
      ElMessage.success('配置已更新')
      currentPath.value = newPath.value
      newPath.value = ''
    } else {
      ElMessage.error(res.message || '更新失败')
    }
  } catch (error) {
    ElMessage.error('更新失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  newPath.value = ''
}
</script>

<style lang="scss" scoped>
.report-path-page {
  .main-card {
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    
    :deep(.el-card__header) {
      background: linear-gradient(135deg, #f8fafb 0%, #ffffff 100%);
      border-bottom: 2px solid #e4e7ed;
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .header-icon {
        font-size: 24px;
        color: #1a5f7a;
      }
      
      .header-title {
        font-size: 18px;
        font-weight: 600;
        color: #303133;
      }
    }
  }
  
  .info-alert {
    margin-bottom: 24px;
    border-radius: 8px;
    
    .alert-title {
      font-weight: 600;
      font-size: 15px;
    }
  }
  
  .form-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 24px 0;
    
    .path-form {
      .current-path-item {
        margin-bottom: 32px;
      }
      
      .new-path-item {
        margin-bottom: 32px;
      }
      
      .button-group {
        margin-bottom: 0;
        
        :deep(.el-form-item__content) {
          justify-content: flex-start;
        }
      }
    }
  }
  
  .current-path-display {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    padding: 20px 24px;
    border-radius: 10px;
    border: 2px solid #bae6fd;
    display: flex;
    align-items: center;
    gap: 12px;
    min-height: 70px;
    transition: all 0.3s;
    
    &:hover {
      border-color: #0284c7;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15);
    }
    
    .path-icon {
      font-size: 24px;
      color: #0284c7;
      flex-shrink: 0;
    }
    
    .path-text {
      flex: 1;
      font-family: 'Courier New', monospace;
      font-size: 15px;
      color: #0c4a6e;
      font-weight: 500;
      word-break: break-all;
      line-height: 1.6;
    }
    
    .status-tag {
      flex-shrink: 0;
      padding: 8px 16px;
      font-weight: 500;
    }
  }
  
  .input-wrapper {
    width: 100%;
    
    .path-input {
      :deep(.el-input__inner) {
        font-family: 'Courier New', monospace;
        font-size: 14px;
      }
    }
  }
  
  .buttons-wrapper {
    display: flex;
    gap: 12px;
    
    .save-button {
      min-width: 140px;
      background: linear-gradient(135deg, #1a5f7a 0%, #159895 100%);
      border: none;
      transition: all 0.3s;
      
      &:hover {
        background: linear-gradient(135deg, #159895 0%, #57c5b6 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 95, 122, 0.3);
      }
      
      &:active {
        transform: translateY(0);
      }
    }
    
    .reset-button {
      min-width: 100px;
    }
  }
  
  .config-guide {
    margin-top: 32px;
    
    .guide-section {
      margin-bottom: 32px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        
        .section-icon {
          font-size: 20px;
          color: #1a5f7a;
        }
        
        h4 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
          color: #1a5f7a;
        }
      }
    }
    
    .examples-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      
      .example-item {
        background: #fafafa;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #e4e7ed;
        transition: all 0.3s;
        
        &:hover {
          border-color: #1a5f7a;
          box-shadow: 0 2px 8px rgba(26, 95, 122, 0.1);
          transform: translateY(-2px);
        }
        
        .el-tag {
          margin-bottom: 10px;
        }
        
        code {
          display: block;
          background: #ffffff;
          padding: 8px 12px;
          border-radius: 6px;
          color: #0c4a6e;
          font-size: 13px;
          border: 1px solid #e2e8f0;
          word-break: break-all;
        }
      }
    }
    
    .notice-list {
      list-style: none;
      padding: 0;
      margin: 0;
      
      li {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        background: #f0fdf4;
        border-radius: 8px;
        border-left: 3px solid #22c55e;
        transition: all 0.3s;
        
        &:hover {
          background: #dcfce7;
          transform: translateX(4px);
        }
        
        .list-icon {
          color: #22c55e;
          font-size: 18px;
          margin-top: 2px;
          flex-shrink: 0;
        }
        
        span {
          color: #606266;
          line-height: 1.6;
        }
      }
    }
  }
}
</style>
