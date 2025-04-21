FROM node:20 as build

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm ci --only=dev

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["node", "index.js"]

FROM layers

ENV NODE_ENV development
ENV PORT 3000