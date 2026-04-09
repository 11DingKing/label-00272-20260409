# QDPS Frontend Admin Dockerfile
# 支持 ARM64 和 AMD64 架构

# 构建阶段
FROM --platform=$BUILDPLATFORM node:20-alpine as builder

WORKDIR /app

# 复制 package.json
COPY package*.json ./

# 安装依赖
RUN npm install --registry=https://registry.npmmirror.com

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 运行阶段 - 使用 nginx 作为静态文件服务器
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
