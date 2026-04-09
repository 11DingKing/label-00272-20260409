<template>
  <div class="certificate-form-page">
    <el-card>
      <template #header>
        <el-icon><Document /></el-icon> {{ isEdit ? '编辑' : '新建' }}质量证明单
      </template>
      
      <!-- 表单编号显示 -->
      <div class="form-number-display">
        {{ formDisplay }}
      </div>
      
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" style="max-width: 800px; margin-top: 20px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="质量证明单号">
              <el-input v-model="form.certificate_number" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="供应商代码">
              <el-input value="203239" disabled />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="产品号" prop="product_number">
              <el-input v-model="form.product_number" placeholder="请输入产品号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品型号" prop="product_model">
              <el-input v-model="form.product_model" placeholder="请输入产品型号" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="批次号" prop="batch_number">
              <el-input v-model="form.batch_number" placeholder="请输入批次号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="零件号" prop="part_number">
              <el-input v-model="form.part_number" placeholder="请输入零件号" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="零件名称" prop="part_name">
              <el-input v-model="form.part_name" placeholder="请输入零件名称" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="数量" prop="quantity">
              <el-input-number v-model="form.quantity" :min="0" :controls="false" placeholder="输入数量" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="单位" prop="unit" label-width="50px">
              <el-input v-model="form.unit" placeholder="件" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="检验日期" prop="inspection_date">
              <el-date-picker v-model="form.inspection_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="检验员" prop="inspector">
              <el-input v-model="form.inspector" placeholder="请输入检验员" />
            </el-form-item>
          </el-col>
          
          <el-col :span="24">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item>
          <el-button type="primary" size="large" :icon="Check" :loading="loading" @click="handleSubmit">保存</el-button>
          <el-button size="large" :icon="Back" @click="$router.push('/certificate')">返回</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, Back } from '@element-plus/icons-vue'
import api from '@/utils/api'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const loading = ref(false)

const isEdit = computed(() => !!route.params.id)
const formDisplay = ref('表单编号：QC-______-20___-______')

const form = reactive({
  certificate_number: '',
  product_number: '',
  product_model: '',
  batch_number: '',
  part_number: '',
  part_name: '',
  quantity: null,
  unit: '件',
  inspection_date: '',
  inspector: '',
  remark: ''
})

const rules = {
  product_number: [{ required: true, message: '请输入产品号', trigger: 'blur' }],
  batch_number: [{ required: true, message: '请输入批次号', trigger: 'blur' }]
}

onMounted(async () => {
  if (isEdit.value) {
    const res = await api.get(`/api/certificate/detail/${route.params.id}`)
    if (res.success) {
      Object.assign(form, res.data)
      // 确保 quantity 是数字类型
      form.quantity = res.data.quantity ? Number(res.data.quantity) : null
      formDisplay.value = res.data.form_display
    }
  } else {
    const res = await api.get('/api/certificate/generate-number')
    if (res.success) {
      form.certificate_number = res.data.certificate_number
      formDisplay.value = res.data.form_display
    }
  }
})

const handleSubmit = async () => {
  await formRef.value?.validate()
  
  loading.value = true
  try {
    const res = isEdit.value
      ? await api.put(`/api/certificate/update/${route.params.id}`, form)
      : await api.post('/api/certificate/create', form)
    
    if (res.success) {
      ElMessage.success(isEdit.value ? '保存成功' : '创建成功')
      router.push('/certificate')
    }
  } finally {
    loading.value = false
  }
}
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

:deep(.el-input-number .el-input__inner) {
  text-align: left;
}
</style>
