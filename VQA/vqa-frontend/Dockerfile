# Frontend Dockerfile

FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install frontend dependencies (including serve)
RUN npm install --save-dev serve
RUN npm install

# Copy all frontend files
COPY . .

# Build React app
RUN npm run build

# Expose frontend port
EXPOSE 3000

RUN ls -la /app && ls -la /app/build

# Serve built frontend using serve
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
