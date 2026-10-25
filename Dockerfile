FROM nginx:alpine

COPY code/index.html /usr/share/nginx/html/index.html
COPY code/style.css /usr/share/nginx/html/style.css

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]