FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

#  Copy the full app code
COPY . .

# Build Next.js
RUN npm run build

# Expose Next.js port
EXPOSE 3000

# Run the app
CMD ["npm", "start"]
