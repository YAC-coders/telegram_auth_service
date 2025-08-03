FROM node:22

WORKDIR /home/app

COPY . .

RUN npm install -g @vue/cli && \
  npm install -g @quasar/cli && \
  npm install -g http-server


RUN npm install

RUN quasar build

CMD [ "http-server", "/home/app/dist/spa" ]
