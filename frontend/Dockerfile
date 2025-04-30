# Stage 1: Build the app
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy project files
COPY . .

# Build Next.js app
RUN npm run build

# Stage 2: Serve the app
FROM node:18-alpine AS runner

# Set working directory
WORKDIR /app

# Copy built assets from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# Install only production dependencies
RUN npm install --only=production

# Expose port
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "start"]
