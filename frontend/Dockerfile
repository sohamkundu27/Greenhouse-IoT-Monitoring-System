# Use Node.js as the base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json /app/
RUN npm install

# Copy the project files
COPY . /app/

# Build the React app
RUN npm run build

# Expose port 3001
EXPOSE 3001

# Serve the app on port 3001
CMD ["npx", "serve", "-s", "build", "-l", "3001"]