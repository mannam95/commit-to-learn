# Get Alpine Linux
FROM node:16.18.1-alpine AS node

# Install bash
RUN apk add --no-cache bash

# Install sudo
RUN apk add --no-cache sudo

# Install git
RUN apk add --no-cache git

# change working directory
WORKDIR /angular

# copy package.json
COPY package.json ./

# Install Angular CLI
RUN npm install -g @angular/cli@14.2.0

# install dependencies
RUN npm install

# Export port 4200
EXPOSE 4200

# start app
CMD ["ng", "serve", "--host", "0.0.0.0"]