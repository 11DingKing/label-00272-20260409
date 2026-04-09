<template>
  <div class="certificate-list-page">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span><el-icon><Document /></el-icon> 质量证明单列表</span>
          <el-button type="primary" @click="$router.push('/certificate/create')">
            <el-icon><Plus /></el-icon>
            <span>新建证明单</span>
          </el-button>
        </div>
      </template>
      
      <!-- 搜索 -->
      <el-form :inline="true" :model="search" class="search-form">
        <el-form-item label="证明单号">
          <el-input v-model="search.certificate_number" placeholder="请输入" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="批次号">
          <el-input v-model="search.batch_number" placeholder="请输入" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="search.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="草稿" :value="0" />
            <el-option label="已提交" :value="1" />
            <el-option label="已审核" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="certificate_number" label="证明单号" width="180" />
        <el-table-column prop="product_number" label="产品号" />
        <el-table-column prop="product_model" label="产品型号" />
        <el-table-column prop="batch_number" label="批次号" min-width="160" show-overflow-tooltip />
        <el-table-column prop="part_number" label="零件号" />
        <el-table-column prop="inspection_date" label="检验日期" width="110" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusTypes[row.status]">{{ row.status_text }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="160" />
        <el-table-column label="操作" width="240" fixed="right" align="center">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" type="info" :icon="View" @click="router.push(`/certificate/view/${row.id}`)">
                查看
              </el-button>
              <template v-if="row.status === 0">
                <el-button size="small" type="primary" :icon="Edit" @click="router.push(`/certificate/edit/${row.id}`)">
                  编辑
                </el-button>
                <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(row)">
                  删除
                </el-button>
              </template>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center">
        <span style="color: #909399">共 {{ pagination.total }} 条记录</span>
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="prev, pager, next"
          @current-change="loadData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { View, Edit, Delete } from '@element-plus/icons-vue'
import api from '@/utils/api'

const router = useRouter()

const loading = ref(false)
const tableData = ref([])
const search = reactive({ certificate_number: '', batch_number: '', status: null })
const pagination = reactive({ page: 1, pageSize: 20, total: 0 })
const statusTypes = { 0: 'warning', 1: 'primary', 2: 'success' }

onMounted(() => loadData())

const loadData = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, page_size: pagination.pageSize, ...search }
    const res = await api.get('/api/certificate/list', { params })
    if (res.success) {
      tableData.value = res.data.items
      pagination.total = res.data.total
    }
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  Object.assign(search, { certificate_number: '', batch_number: '', status: null })
  pagination.page = 1
  loadData()
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定要删除该证明单吗？', '警告', { type: 'warning' })
  const res = await api.delete(`/api/certificate/delete/${row.id}`)
  if (res.success) {
    ElMessage.success('删除成功')
    loadData()
  }
}
</script>

<style lang="scss" scoped>
.certificate-list-page {
  .action-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }
  
  .search-form {
    margin-bottom: 16px;
  }
}
</style>
