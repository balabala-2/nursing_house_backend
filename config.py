from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from controller.login import router as login_router
from controller.user_manage import router as elderly_router
from controller.video import router as video_router
from controller.event import router as chart_router

# 初始化服务器
def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI()
    # 其余的一些全局配置可以写在这里 多了可以考虑拆分到其他文件夹
    # 跨域设置
    register_cors(app)
    # 注册路由
    register_router(app)
    return app


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(login_router)
    app.include_router(video_router)
    app.include_router(elderly_router)
    app.include_router(chart_router)


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
