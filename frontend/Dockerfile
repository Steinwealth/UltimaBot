# Use Node.js LTS image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy rest of frontend code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite development server
CMD ["npm", "run", "dev"]
