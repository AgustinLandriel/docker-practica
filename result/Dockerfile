FROM node:alpine
USER node
LABEL worker="worker"
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "main.js"]