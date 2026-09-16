# my-playwright-folder/Dockerfile
FROM mcr.microsoft.com/playwright:v1.49.0-noble

WORKDIR /app

# Everything copied here is strictly from my-playwright-folder
COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npx", "playwright", "test"]
