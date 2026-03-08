
#-- dev stage ---
FROM node:lts AS dev
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]



#---prod stage----
FROM node:lts AS prod
WORKDIR /app
COPY package*.json .
RUN npm ci
RUN npm install  --production
COPY . .
RUN npm run build
CMD ["npm", "start"]