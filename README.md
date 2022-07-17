# nursing_house_backend


智能养老系统后端部分

该系统后端采用python fastapi框架搭建，主要目的是算法的整合与各服务接口的实现

具体模块的介绍如下：

- algorithm：算法部分
- controller：接口层
- dao：数据访问层/
- service：业务逻辑层
- schemas：自定义的交互时的数据结构
- -resources：外部资源

https://fastapi.tiangolo.com/zh/

将代码clone到本地后，需执行以下命令：

pip install fastapi

pip install uvicorn[standard]

通过以下命令运行：

uvicorn main:app --reload
