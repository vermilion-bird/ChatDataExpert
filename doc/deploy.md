1. 修改nginx配置文件增加域名配置
server {
    listen 80;
    server_name bluevision.aib.lol;
    root  /usr/share/nginx/html/dist/chatDataExpert;
    index index.html;
    location /api/v1 {
            proxy_pass http://172.17.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
    }
}
2. 复制配置文件到docker容器下nginx配置目录
 sudo docker cp nginx/conf/default.conf 000b5cc46e7b9:/etc/nginx/conf.d/default.conf
3. 复制静态文件到docker容器下nginx配置目录
 # 本地执行,复制文件到本地挂载目录
 cp -r dist/* ../../web/dist/chatDataExpert/
 # 复制文件到docker容器
 sudo docker cp dist/chatData 000b5cc46e7b9:/usr/share/nginx/html/dist/chatData
3. 重启nginx容器
 sudo docker restart 000b5cc46e7b9
# 查看容器ip
 sudo docker inspect 000b5cc46e7 | grep '"IPAddress":' | awk -F '"' '{print $4}


 # guicorn启动

 pip install gunicorn
 - 设置超时时间为5分钟
 nohup gunicorn --timeout 300 -w 6 -b 172.17.0.1:8000 app:app >>./OSlog 2>&1 &
