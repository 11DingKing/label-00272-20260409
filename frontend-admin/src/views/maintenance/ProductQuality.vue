<template>
  <div class="product-quality-page">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span><el-icon><Coin /></el-icon> 产品检测数据维护</span>
          <el-button type="primary" @click="showDialog()">
            <el-icon><Plus /></el-icon>
            <span>新增数据</span>
          </el-button>
        </div>
      </template>
      
      <!-- 搜索 -->
      <el-form :inline="true" :model="search" class="search-form">
        <el-form-item label="产品号">
          <el-input v-model="search.product_number" placeholder="请输入" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="批次号">
          <el-input v-model="search.batch_number" placeholder="请输入" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="serial_number" label="序号" width="80" />
        <el-table-column prop="product_number" label="产品号" width="120" />
        <el-table-column prop="batch_number" label="批次号" width="120" />
        <el-table-column prop="three_motion_meas_data_path" label="三动数据路径" show-overflow-tooltip />
        <el-table-column prop="four_motion_meas_data_path" label="四动数据路径" show-overflow-tooltip />
        <el-table-column prop="five_motion_meas_data_path" label="五动数据路径" show-overflow-tooltip />
        <el-table-column prop="create_time" label="创建时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" type="primary" :icon="Edit" @click="showDialog(row)">
                编辑
              </el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(row)">
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <div style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center">
        <span style="color: #909399">共 {{ pagination.total }} 条记录</span>
        <el-pagination v-model:current-page="pagination.page" :page-size="pagination.pageSize" :total="pagination.total" layout="prev, pager, next" @current-change="loadData" />
      </div>
    </el-card>
    
    <!-- 编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogForm.serial_number ? '编辑数据' : '新增数据'" width="600px">
      <el-form ref="dialogFormRef" :model="dialogForm" :rules="dialogRules" label-width="140px">
        <el-form-item label="产品号" prop="product_number">
          <el-input v-model="dialogForm.product_number" placeholder="请输入产品号" />
        </el-form-item>
        <el-form-item label="批次号" prop="batch_number">
          <el-input v-model="dialogForm.batch_number" placeholder="请输入批次号" :disabled="!!dialogForm.serial_number" />
        </el-form-item>
        <el-form-item label="三动实测数据路径">
          <el-input v-model="dialogForm.three_motion_path" placeholder="D:\Data\三动\批次001" />
        </el-form-item>
        <el-form-item label="四动实测数据路径">
          <el-input v-model="dialogForm.four_motion_path" placeholder="D:\Data\四动\批次001" />
        </el-form-item>
        <el-form-item label="五动实测数据路径">
          <el-input v-model="dialogForm.five_motion_path" placeholder="D:\Data\五动\批次001" />
        </el-form-item>
        <el-form-item label="叶型扫描数据路径">
          <el-input v-model="dialogForm.blade_profile_path" placeholder="D:\Data\叶型扫描\批次001" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="dialogLoading" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'
import api from '@/utils/api'

const loading = ref(false)
const tableData = ref([])
const search = reactive({ product_number: '', batch_number: '' })
const pagination = reactive({ page: 1, pageSize: 20, total: 0 })

const dialogVisible = ref(false)
const dialogLoading = ref(false)
const dialogFormRef = ref()
const dialogForm = reactive({
  serial_number: null,
  product_number: '',
  batch_number: '',
  three_motion_path: '',
  four_motion_path: '',
  five_motion_path: '',
  blade_profile_path: ''
})
const dialogRules = {
  product_number: [{ required: true, message: '请输入产品号', trigger: 'blur' }],
  batch_number: [{ required: true, message: '请输入批次号', trigger: 'blur' }]
}

onMounted(() => loadData())

const loadData = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, page_size: pagination.pageSize, ...search }
    const res = await api.get('/api/maintenance/product-quality/list', { params })
    if (res.success) {
      tableData.value = res.data.items
      pagination.total = res.data.total
    }
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  Object.assign(search, { product_number: '', batch_number: '' })
  pagination.page = 1
  loadData()
}

const showDialog = (row = null) => {
  if (row) {
    Object.assign(dialogForm, {
      serial_number: row.serial_number,
      product_number: row.product_number,
      batch_number: row.batch_number,
      three_motion_path: row.three_motion_meas_data_path,
      four_motion_path: row.four_motion_meas_data_path,
      five_motion_path: row.five_motion_meas_data_path,
      blade_profile_path: row.blade_profile_scan_data_path
    })
  } else {
    Object.assign(dialogForm, {
      serial_number: null, product_number: '', batch_number: '',
      three_motion_path: '', four_motion_path: '', five_motion_path: '', blade_profile_path: ''
    })
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  await dialogFormRef.value?.validate()
  
  dialogLoading.value = true
  try {
    const res = dialogForm.serial_number
      ? await api.put(`/api/maintenance/product-quality/${dialogForm.serial_number}`, dialogForm)
      : await api.post('/api/maintenance/product-quality/create', dialogForm)
    
    if (res.success) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      loadData()
    }
  } finally {
    dialogLoading.value = false
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定要删除该数据吗？', '警告', { type: 'warning' })
  const res = await api.delete(`/api/maintenance/product-quality/${row.serial_number}`)
  if (res.success) {
    ElMessage.success('删除成功')
    loadData()
  }
}
</script>

<style lang="scss" scoped>
.product-quality-page {
  .action-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
  }
  
  .search-form {
    margin-bottom: 16px;
  }
}
</style>