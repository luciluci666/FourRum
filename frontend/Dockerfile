FROM node:18-alpine
ENV NODE_ENV=development

WORKDIR /var/www/html
COPY .. .

RUN npm install
CMD npm run web