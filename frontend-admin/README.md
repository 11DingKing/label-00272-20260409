# QDPS 前端管理后台

基于 Vue 3 + Vite + Element Plus 的现代化单页应用，提供质量数据处理系统的 Web 界面。

## 技术栈

- **框架：** Vue 3.4.15 (Composition API)
- **构建工具：** Vite 5.0.11
- **UI 组件库：** Element Plus 2.5.3
- **图标库：** @element-plus/icons-vue 2.3.1
- **路由：** Vue Router 4.2.5
- **状态管理：** Pinia 2.1.7
- **HTTP 客户端：** Axios 1.6.5
- **样式预处理：** Sass 1.70.0

## 项目结构

```
frontend-admin/
├── public/
│   └── favicon.svg          # 网站图标
├── src/
│   ├── layouts/             # 布局组件
│   │   └── MainLayout.vue  # 主布局（侧边栏+内容区）
│   ├── router/              # 路由配置
│   │   └── index.js        # 路由定义和守卫
│   ├── stores/              # Pinia 状态管理
│   │   └── user.js         # 用户状态（登录、Token）
│   ├── styles/              # 全局样式
│   │   └── main.scss       # 主样式文件（CSS 变量、主题）
│   ├── utils/               # 工具函数
│   │   └── api.js          # Axios 封装（拦截器）
│   ├── views/               # 页面组件
│   │   ├── Home.vue        # 首页（功能卡片）
│   │   ├── Login.vue       # 登录页
│   │   ├── certificate/    # 质量证明单模块
│   │   │   ├── List.vue   # 证明单列表
│   │   │   ├── Form.vue   # 创建/编辑表单
│   │   │   └── View.vue   # 证明单详情
│   │   ├── dimension/      # 尺寸判定模块
│   │   │   └── MotionCheck.vue  # 判定页面（三动/四动/五动）
│   │   └── maintenance/    # 维护模块
│   │       ├── ProductQuality.vue  # 产品质量数据维护
│   │       └── ReportPath.vue      # 报告路径维护
│   ├── App.vue              # 根组件
│   └── main.js              # 应用入口
├── index.html               # HTML 模板
├── vite.config.js           # Vite 配置
├── package.json             # 依赖配置
├── nginx.conf               # Nginx 配置（Docker）
└── Dockerfile              # Docker 镜像构建

```

## 快速开始

### 本地开发

```bash
# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev
```

访问 http://localhost:8081

### 生产构建

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

构建产物输出到 `dist/` 目录

### Docker 部署

```bash
# 构建镜像
docker build -t qdps-frontend .

# 运行容器
docker run -p 8081:80 qdps-frontend
```

## 配置说明

### Vite 配置 (`vite.config.js`)

```javascript
{
  server: {
    host: '0.0.0.0',
    port: 8081,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',  // 后端地址
        changeOrigin: true
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')  // @ 映射到 src 目录
    }
  }
}
```

### 环境变量

创建 `.env.local` 文件（可选）：

```bash
VITE_API_BASE_URL=http://localhost:5001
```

## 路由结构

```
/                           # 主布局
├── /                      # 首页（功能卡片）
├── /dimension/three       # 三动全尺寸判定
├── /dimension/four        # 四动全尺寸判定
├── /dimension/five        # 五动全尺寸判定
├── /certificate           # 质量证明单列表
├── /certificate/create    # 创建证明单
├── /certificate/edit/:id  # 编辑证明单
├── /certificate/view/:id  # 查看证明单
├── /maintenance/product-quality  # 产品质量数据维护
└── /maintenance/report-path      # 报告路径维护

/login                     # 登录页（独立布局）
```

### 路由守卫

- **登录拦截：** 未登录用户访问需认证页面自动跳转到 `/login`
- **登录跳转：** 已登录用户访问 `/login` 自动跳转到首页
- **Token 验证：** 通过 Pinia Store 的 `isLoggedIn` 计算属性判断

## 状态管理

### User Store (`stores/user.js`)

```javascript
{
  token: string,           // JWT Token
  user: {                  // 用户信息
    id: number,
    username: string,
    display_name: string,
    department: string,
    email: string
  },
  isLoggedIn: boolean,     // 计算属性：是否已登录
  
  // 方法
  login(username, password),  // 登录
  logout()                    // 登出
}
```

数据持久化到 `localStorage`：
- `token` → localStorage.token
- `user` → localStorage.user (JSON)

## API 请求

### Axios 封装 (`utils/api.js`)

**请求拦截器：**
- 自动从 localStorage 读取 Token
- 添加 `Authorization: Bearer <token>` 请求头

**响应拦截器：**
- 自动提取 `response.data`
- 401 错误处理：清除 Token → 显示提示 → 跳转登录页（延迟 500ms）
- 其他错误：显示 ElMessage 错误提示

**使用示例：**

```javascript
import api from '@/utils/api'

// GET 请求
const res = await api.get('/api/dimension/batch-numbers')

// POST 请求
const res = await api.post('/api/auth/login', {
  username: 'admin',
  password: 'admin123'
})

// 响应格式
{
  success: boolean,
  message: string,
  data: any
}
```

## 样式系统

### CSS 变量 (`styles/main.scss`)

```scss
:root {
  --primary-color: #1a5f7a;      // 主色调（深青色）
  --secondary-color: #159895;    // 辅助色（青绿色）
  --accent-color: #57c5b6;       // 强调色（浅青色）
  --bg-dark: #0a2647;            // 深色背景
  --bg-light: #f5f7fa;           // 浅色背景
}
```

### 全局样式类

- `.page-container` - 页面容器（padding: 20px）
- `.card` - 卡片样式（白色背景、圆角、阴影）
- `.page-header` - 页面标题（flex 布局）
- `.search-form` - 搜索表单（浅灰背景）
- `.action-buttons` - 表格操作列（flex + gap）
- `.result-card.pass` - 合格结果卡片（绿色左边框）
- `.result-card.fail` - 不合格结果卡片（红色左边框）

### Element Plus 主题定制

```scss
.el-button--primary {
  --el-button-bg-color: var(--primary-color);
  --el-button-hover-bg-color: var(--secondary-color);
}
```

## 组件开发

### 页面组件模板

```vue
<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="page-header">
          <h2>页面标题</h2>
          <el-button type="primary">操作按钮</el-button>
        </div>
      </template>
      
      <!-- 页面内容 -->
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'

// 响应式数据
const loading = ref(false)
const dataList = ref([])

// 生命周期
onMounted(async () => {
  await fetchData()
})

// 方法
const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/xxx')
    if (res.success) {
      dataList.value = res.data
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
// 组件样式
</style>
```

### 表格操作列按钮

```vue
<el-table-column label="操作" width="180" fixed="right">
  <template #default="{ row }">
    <div class="action-buttons">
      <el-button 
        type="primary" 
        size="small" 
        :icon="Edit"
        @click="handleEdit(row)"
      >
        编辑
      </el-button>
      <el-button 
        type="danger" 
        size="small" 
        :icon="Delete"
        @click="handleDelete(row)"
      >
        删除
      </el-button>
    </div>
  </template>
</el-table-column>
```

## 功能模块

### 1. 登录认证

- **页面：** `views/Login.vue`
- **功能：** 用户名密码登录、记住登录状态
- **流程：** 输入凭证 → 调用登录 API → 保存 Token → 跳转首页

### 2. 首页

- **页面：** `views/Home.vue`
- **功能：** 显示欢迎信息和功能卡片
- **特点：** 卡片式布局、渐变图标、悬停动画

### 3. 尺寸判定

- **页面：** `views/dimension/MotionCheck.vue`
- **功能：** 选择批次号 → 执行判定 → 查看结果 → 下载报告
- **特点：** 
  - 通过 props 区分三动/四动/五动
  - 批次号下拉框支持搜索
  - 判定结果表格展示
  - 下载按钮使用 fetch API 避免打开 JSON 页面

### 4. 质量证明单

- **页面：** `views/certificate/List.vue`、`Form.vue`、`View.vue`
- **功能：** 列表查询、创建、编辑、查看、删除、提交
- **特点：**
  - 状态标签（草稿/已提交/已审批）
  - 表单验证
  - 单号自动生成

### 5. 产品质量数据维护

- **页面：** `views/maintenance/ProductQuality.vue`
- **功能：** 产品检测数据的增删改查
- **特点：** 批次号唯一性校验

### 6. 报告路径维护

- **页面：** `views/maintenance/ReportPath.vue`
- **功能：** 配置报告存储路径
- **特点：** 当前路径显示、状态标签

## 交互细节

### 动画效果

- **按钮悬停：** `transform: translateY(-2px)` + 阴影加深
- **卡片悬停：** `transform: translateY(-4px)` + 阴影加深
- **结果卡片入场：** `@keyframes slideIn`（从下方滑入）
- **下载图标弹跳：** `@keyframes bounce`（上下弹跳）
- **光泽扫过：** `::before` 伪元素从左到右移动

### 用户反馈

- **成功操作：** `ElMessage.success('操作成功')`
- **错误提示：** `ElMessage.error('错误信息')`
- **警告提示：** `ElMessage.warning('警告信息')`
- **加载状态：** `loading` 变量控制按钮和表格加载状态
- **确认对话框：** `ElMessageBox.confirm()` 用于删除等危险操作

### 表单验证

```javascript
const rules = {
  batch_number: [
    { required: true, message: '请输入批次号', trigger: 'blur' },
    { pattern: /^[A-Z0-9-]+$/, message: '格式不正确', trigger: 'blur' }
  ]
}
```

## 开发规范

### 命名规范

- **组件文件：** PascalCase（如 `ProductQuality.vue`）
- **路由名称：** PascalCase（如 `ProductQuality`）
- **变量/方法：** camelCase（如 `batchNumber`、`handleSubmit`）
- **常量：** UPPER_SNAKE_CASE（如 `API_BASE_URL`）

### 代码风格

- 使用 Composition API（`<script setup>`）
- 优先使用 `const`，避免 `var`
- 使用 ES6+ 语法（箭头函数、解构、模板字符串）
- 异步操作使用 `async/await`
- 组件样式使用 `scoped`

### 注释规范

```javascript
/**
 * 执行尺寸判定
 * @param {string} batchNumber - 批次号
 * @param {string} motionType - 运动类型（三动/四动/五动）
 */
const handleCheck = async () => {
  // 实现逻辑
}
```

## 构建优化

### Vite 优化

- **代码分割：** 路由懒加载（`() => import()`）
- **资源压缩：** 自动压缩 JS/CSS/HTML
- **Tree Shaking：** 自动移除未使用代码
- **缓存优化：** 文件名包含 hash 值

### 性能优化

- **图标按需引入：** 全局注册常用图标
- **组件懒加载：** 路由级别代码分割
- **请求优化：** Axios 拦截器统一处理
- **状态持久化：** localStorage 减少重复请求

## 浏览器兼容性

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

> 不支持 IE 浏览器

## 常见问题

### Q: 如何修改后端 API 地址？
A: 编辑 `vite.config.js` 中的 `proxy.target` 或设置 `VITE_API_BASE_URL` 环境变量。

### Q: 如何添加新页面？
A: 
1. 在 `src/views/` 创建组件
2. 在 `src/router/index.js` 添加路由
3. 在首页或菜单添加入口

### Q: 如何自定义主题色？
A: 修改 `src/styles/main.scss` 中的 CSS 变量。

### Q: Token 过期怎么办？
A: Axios 拦截器会自动处理，显示提示并跳转登录页。

### Q: 如何调试 API 请求？
A: 打开浏览器开发者工具 → Network 标签页查看请求详情。

## 部署说明

### Nginx 配置

生产环境使用 Nginx 托管静态文件：

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker 部署

多阶段构建，减小镜像体积：

1. **构建阶段：** 使用 Node.js 镜像构建
2. **运行阶段：** 使用 Nginx 镜像托管静态文件

## 许可证

内部项目，仅供公司内部使用。
