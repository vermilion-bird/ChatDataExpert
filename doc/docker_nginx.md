## 启动容器
```
sudo docker run --name nginx -d -p 80:80 -v /home/ubuntu/web/dist/:/usr/share/nginx/html/dist/ -v /home/ubuntu/log/nginx:/var/log/nginx/ nginx
```
## 复制配置文件到docker容器下nginx配置目录
```
sudo docker cp nginx/conf/default.conf nginx:/etc/nginx/conf.d/default.conf
```
# 重启容器
sudo docker container restart nginx 