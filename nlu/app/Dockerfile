# install main packages
FROM node:16-alpine

# working directory
WORKDIR /opt/app

# expose port
EXPOSE 4000

# Copy resources
COPY route.js /opt/app
COPY backend.js /opt/app
COPY index.js /opt/app
COPY index.html /opt/app

# define environment
RUN npm init -y

# install dependencies
RUN npm install express

# insert in the global path
RUN export PATH=$PATH:/opt/app

# running server
CMD ["node", "backend.js"]
