FROM node:16-alpine
ENV NODE_ENV=development

WORKDIR /var/www/html
COPY .. .

RUN npm i -g expo-cli@latest
RUN npm install
CMD npm run web