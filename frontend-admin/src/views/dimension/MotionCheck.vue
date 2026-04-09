<template>
  <div class="motion-check-page">
    <!-- 判定表单 -->
    <el-card>
      <template #header>
        <el-icon><DataLine /></el-icon> {{ motionType }}全尺寸判定
      </template>
      
      <el-form :model="form" label-width="100px" class="check-form">
        <el-card shadow="never" class="form-card">
          <el-row :gutter="24">
            <el-col :span="12">
              <el-form-item label="批次号" required>
                <el-select 
                  v-model="form.batchNumber" 
                  filterable 
                  placeholder="请选择批次号" 
                  size="large"
                  style="width: 100%" 
                  @change="handleBatchChange"
                >
                  <el-option 
                    v-for="item in batchList" 
                    :key="item.BatchNumber" 
                    :label="`${item.BatchNumber} (${item.ProductNumber})`" 
                    :value="item.BatchNumber" 
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="产品号">
                <el-input v-model="batchInfo.ProductNumber" size="large" disabled />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item :label="`${motionType}数据路径`" v-if="batchInfo.dataPath">
            <el-input :value="batchInfo.dataPath" size="large" disabled>
              <template #prefix>
                <el-icon><FolderOpened /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-divider />
          
          <el-form-item class="button-group">
            <el-button 
              class="check-button" 
              type="primary" 
              size="large" 
              :loading="loading" 
              @click="handleCheck"
            >
              <el-icon><VideoPlay /></el-icon> 
              <span>开始判定</span>
            </el-button>
          </el-form-item>
        </el-card>
      </el-form>
    </el-card>
    
    <!-- 判定结果 -->
    <el-card v-if="result" class="result-card" :class="result.passed ? 'pass' : 'fail'" style="margin-top: 20px">
      <template #header>
        <el-icon><Checked /></el-icon> 判定结果
      </template>
      
      <div class="result-summary">
        <div class="result-icon">
          <el-icon size="40" :color="result.passed ? '#67c23a' : '#f56c6c'">
            <component :is="result.passed ? 'CircleCheckFilled' : 'CircleCloseFilled'" />
          </el-icon>
        </div>
        <div class="result-info">
          <h3 :style="{ color: result.passed ? '#67c23a' : '#f56c6c' }">{{ result.summary.overall_result }}</h3>
          <p>批次号: {{ result.summary.batch_number }} | 产品号: {{ result.summary.product_number }} | 文件数: {{ result.summary.files_processed }} | 合格: {{ result.summary.files_passed }} | 不合格: {{ result.summary.files_failed }}</p>
        </div>
      </div>
      
      <el-table :data="result.details" stripe style="margin-top: 20px">
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="passed" label="判定结果" width="100">
          <template #default="{ row }">
            <el-tag :type="row.passed ? 'success' : 'danger'">{{ row.passed ? '合格' : '不合格' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_items" label="检测项总数" width="100" />
        <el-table-column prop="passed_items" label="合格项数" width="100" />
        <el-table-column prop="failed_items" label="不合格项数" width="100" />
        <el-table-column prop="details" label="详情" show-overflow-tooltip />
      </el-table>
      
      <div class="download-section" v-if="result.report_filename">
        <el-button 
          class="download-button" 
          type="success" 
          size="large"
          @click="downloadReport"
        >
          <el-icon><Download /></el-icon> 
          <span>下载判定报告</span>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'

const props = defineProps({
  motionType: { type: String, required: true }
})

const loading = ref(false)
const batchList = ref([])
const form = reactive({ batchNumber: '' })
const batchInfo = reactive({ ProductNumber: '', dataPath: '' })
const result = ref(null)

const pathKeyMap = { '三动': 'ThreeMotionMeasDataPath', '四动': 'FourMotionMeasDataPath', '五动': 'FiveMotionMeasDataPath' }
const apiMap = { '三动': 'three-motion', '四动': 'four-motion', '五动': 'five-motion' }

// 监听 motionType 变化，切换时清空数据
watch(() => props.motionType, () => {
  // 清空表单数据
  form.batchNumber = ''
  batchInfo.ProductNumber = ''
  batchInfo.dataPath = ''
  // 清空结果数据
  result.value = null
})

onMounted(async () => {
  const res = await api.get('/api/dimension/batch-numbers')
  if (res.success) batchList.value = res.data
})

const handleBatchChange = async (val) => {
  if (!val) return
  const res = await api.get(`/api/dimension/batch-info/${val}`)
  if (res.success) {
    batchInfo.ProductNumber = res.data.ProductNumber
    batchInfo.dataPath = res.data[pathKeyMap[props.motionType]]
  }
}

const handleCheck = async () => {
  if (!form.batchNumber) {
    ElMessage.warning('请先选择批次号')
    return
  }
  
  loading.value = true
  result.value = null
  try {
    const res = await api.post(`/api/dimension/check/${apiMap[props.motionType]}`, { batch_number: form.batchNumber })
    if (res.success) {
      result.value = res
    } else {
      ElMessage.error(res.message)
    }
  } finally {
    loading.value = false
  }
}

const downloadReport = async () => {
  if (result.value?.report_filename) {
    try {
      ElMessage.success('正在下载报告...')
      
      // 使用axios下载，这样可以通过拦截器处理401
      const token = localStorage.getItem('token')
      const response = await fetch(`/api/dimension/download/${result.value.report_filename}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.status === 401) {
        ElMessage.error('登录已过期，请重新登录')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        setTimeout(() => {
          window.location.href = '/login'
        }, 500)
        return
      }
      
      if (!response.ok) {
        ElMessage.error('下载失败')
        return
      }
      
      // 创建下载链接
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = result.value.report_filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('下载失败:', error)
      ElMessage.error('下载失败')
    }
  }
}
</script>

<style lang="scss" scoped>
.motion-check-page {
  .check-form {
    .form-card {
      background: linear-gradient(to bottom, #ffffff, #f8fafb);
      border: 1px solid #e4e7ed;
      border-radius: 12px;
      padding: 24px;
      
      :deep(.el-form-item__label) {
        font-weight: 500;
        color: #303133;
      }
      
      :deep(.el-input.is-disabled .el-input__inner) {
        background-color: #f5f7fa;
        color: #606266;
      }
      
      :deep(.el-divider) {
        margin: 24px 0;
      }
    }
  }
  
  .button-group {
    text-align: center;
    margin-bottom: 0;
    
    :deep(.el-form-item__content) {
      display: flex;
      justify-content: center;
    }
  }
  
  .check-button {
    width: 280px;
    height: 60px;
    font-size: 20px;
    font-weight: 600;
    border-radius: 30px;
    box-shadow: 0 6px 20px rgba(26, 95, 122, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: linear-gradient(135deg, #1a5f7a 0%, #159895 100%);
    border: none;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      transition: left 0.6s;
    }
    
    &:hover {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 10px 30px rgba(26, 95, 122, 0.35);
      background: linear-gradient(135deg, #159895 0%, #57c5b6 100%);
      
      &::before {
        left: 100%;
      }
    }
    
    &:active {
      transform: translateY(-1px) scale(1);
      box-shadow: 0 4px 15px rgba(26, 95, 122, 0.3);
    }
    
    .el-icon {
      font-size: 24px;
      margin-right: 12px;
    }
  }
  
  .download-section {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px dashed #e4e7ed;
    text-align: center;
  }
  
  .download-button {
    min-width: 240px;
    height: 54px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 27px;
    box-shadow: 0 4px 16px rgba(103, 194, 58, 0.25);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
    border: none;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      transition: left 0.6s;
    }
    
    &:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 8px 24px rgba(103, 194, 58, 0.35);
      background: linear-gradient(135deg, #85ce61 0%, #95d475 100%);
      
      &::before {
        left: 100%;
      }
    }
    
    &:active {
      transform: translateY(0) scale(1);
      box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
    }
    
    .el-icon {
      font-size: 20px;
      margin-right: 10px;
      animation: bounce 2s infinite;
    }
  }
}

.result-card {
  &.pass { 
    border-left: 4px solid #67c23a;
    animation: slideIn 0.4s ease-out;
  }
  &.fail { 
    border-left: 4px solid #f56c6c;
    animation: slideIn 0.4s ease-out;
  }
}

.result-summary {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #fafafa 0%, #f0f2f5 100%);
  border-radius: 12px;
  
  h3 { 
    margin: 0 0 8px; 
    font-size: 22px;
    font-weight: 600;
  }
  p { 
    margin: 0; 
    color: #606266;
    font-size: 14px;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
</style>
