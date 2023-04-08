FROM centos:7.6.1810

WORKDIR /usr/src/app

ENV LANG en_US.utf8

# 设置时间
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

# 安装python3
RUN yum install -y centos-release-scl
RUN yum install -y rh-python38
RUN ln -s /opt/rh/rh-python38/root/usr/bin/python3 /usr/bin/python3
RUN ln -s /opt/rh/rh-python38/root/usr/bin/pip3 /usr/bin/pip3

# 添加项目并设置工作目录
COPY . .

# 安装python第三方库
RUN /usr/bin/pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

EXPOSE 8000

CMD ["/usr/bin/python3","manage.py","runserver","0:8000"]