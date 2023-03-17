FROM node:16-alpine

ARG NODE_ENV=development
ENV NODE_ENV $NODE_ENV


ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH /home/node/.npm-global/bin:$PATH
RUN npm i --unsafe-perm --allow-root -g npm@latest expo-cli@latest

ENV PATH /opt/.bin:$PATH

WORKDIR /opt/app
COPY . .

RUN npm install

CMD npm run web