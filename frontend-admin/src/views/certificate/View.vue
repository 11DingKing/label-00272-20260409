<template>
  <div class="certificate-view-page">
    <el-card v-loading="loading">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span><el-icon><Document /></el-icon> 质量证明单详情</span>
          <el-tag :type="statusTypes[data.status]">{{ data.status_text }}</el-tag>
        </div>
      </template>
      
      <div class="form-number-display">{{ data.form_display }}</div>
      
      <el-descriptions :column="2" border style="margin-top: 20px">
        <el-descriptions-item label="质量证明单号">{{ data.certificate_number }}</el-descriptions-item>
        <el-descriptions-item label="供应商代码">{{ data.supplier_code }}</el-descriptions-item>
        <el-descriptions-item label="产品号">{{ data.product_number || '-' }}</el-descriptions-item>
        <el-descriptions-item label="产品型号">{{ data.product_model || '-' }}</el-descriptions-item>
        <el-descriptions-item label="批次号">{{ data.batch_number || '-' }}</el-descriptions-item>
        <el-descriptions-item label="零件号">{{ data.part_number || '-' }}</el-descriptions-item>
        <el-descriptions-item label="零件名称">{{ data.part_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="数量">{{ data.quantity || '-' }} {{ data.unit }}</el-descriptions-item>
        <el-descriptions-item label="检验日期">{{ data.inspection_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="检验员">{{ data.inspector || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ data.creator || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ data.create_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ data.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
      
      <div style="margin-top: 20px; display: flex; gap: 12px;">
        <el-button :icon="Back" @click="$router.push('/certificate')">返回列表</el-button>
        <el-button type="primary" :icon="Edit" v-if="data.status === 0" @click="$router.push(`/certificate/edit/${route.params.id}`)">编辑</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Back, Edit } from '@element-plus/icons-vue'
import api from '@/utils/api'

const route = useRoute()
const loading = ref(false)
const data = reactive({})
const statusTypes = { 0: 'warning', 1: 'primary', 2: 'success' }

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get(`/api/certificate/detail/${route.params.id}`)
    if (res.success) Object.assign(data, res.data)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.form-number-display {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  padding: 16px 24px;
  border-radius: 8px;
  border: 2px dashed #cbd5e1;
  font-size: 16px;
  font-weight: 600;
  color: #1a5f7a;
  font-family: 'Courier New', monospace;
}
</style>
