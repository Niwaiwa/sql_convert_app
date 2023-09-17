FROM node:20-bullseye-slim

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

RUN yarn build

CMD ["yarn", "start"]
