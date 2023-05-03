要使用 Docker 启动 MySQL 容器并允许远程访问，请按照以下步骤操作：

1. 拉取官方 MySQL 镜像

在终端中运行以下命令来拉取官方 MySQL 镜像：

```bash
docker pull mysql:latest
```

2. 启动 MySQL 容器

运行以下命令以使用自定义配置文件启动 MySQL 容器。这将创建一个名为 `my_mysql` 的容器，并将本地端口 3306 映射到容器的端口 3306。请确保将 `MYSQL_ROOT_PASSWORD` 替换为您自己的强密码。

```bash
docker run --name mysql_bv -p 3306:3306 -e MYSQL_ROOT_PASSWORD='' -d mysql:latest
```

3. 修改 MySQL 配置

首先，进入容器：

```bash
docker exec -it my_mysql bash
```

然后，使用 vi 编辑器（或您喜欢的任何其他编辑器）编辑 MySQL 配置文件 `/etc/mysql/mysql.conf.d/mysqld.cnf`：

```bash
vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

找到 `bind-address` 这一行并注释掉它，以允许 MySQL 从任何 IP 地址接收连接。如果找不到这一行，可以直接添加到文件末尾：

```ini
# bind-address = 127.0.0.1
```

保存文件并退出编辑器。

4. 重启 MySQL 服务

```bash
mysqladmin -uroot -p shutdown
```

输入您在第2步中设置的 `MYSQL_ROOT_PASSWORD`，然后重启容器：

```bash
docker restart my_mysql
```

5. 修改 root 用户允许远程连接

在容器中运行以下命令以连接到 MySQL：

```bash
mysql -uroot -p
```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'username' WITH GRANT OPTION;

CREATE USER 'username'@'%' IDENTIFIED WITH mysql_native_password BY 'username';
GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' WITH GRANT OPTION;




输入您在第2步中设置的 `MYSQL_ROOT_PASSWORD`，然后运行以下命令以允许 root 用户从任何 IP 地址远程连接：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'username' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
```


现在，您应该能够从任何远程计算机访问此 MySQL 容器。请确保您的防火墙允许通过 3306 端口的入站连接。注意，允许 root 用户从任何 IP 地址连接可能带来安全风险，因此请谨慎操作。在生产环境中，建议创建单独的用户并授予适当的权限。