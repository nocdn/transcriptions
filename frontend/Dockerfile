# Stage 1: Build the frontend
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the frontend
FROM python:3.11-slim AS final
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3090
COPY ./uvicorn_entrypoint.sh /app/uvicorn_entrypoint.sh
RUN chmod +x /app/uvicorn_entrypoint.sh
ENTRYPOINT ["/app/uvicorn_entrypoint.sh"]
