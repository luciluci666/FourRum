FROM node:18-alpine
ENV NODE_ENV=development

WORKDIR /var/www/html
COPY .. .

RUN npm i --unsafe-perm --allow-root -g expo-cli@latest
RUN npm install
RUN npx expo-cli upgrade
CMD npm run web