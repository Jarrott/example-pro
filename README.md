## 城南大数据平台项目

### 架构与代码重构


> 运行服务的话需要在config目录下新建一个“securecrt”文件，并填入对应的mysql信息

### 运行服务
1.首先将“77.art”加入到自己电脑的hosts中

2.将项目下载好后，运行bigdata.py即可。

3.在 Dockerfile 中安装依赖，加--system参数表示使用 pip 直接安装相应依赖，不创建虚拟环境。

 `RUN pipenv install --deploy --system`

### 项目API接口展示

http://77.art:5000/apidocs