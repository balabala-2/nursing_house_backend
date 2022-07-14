from datetime import datetime
from datetime import timedelta
from typing import Any, Union, Optional

from fastapi import Header
import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 1

SECRET_KEY = "kkkkk"
ALGORITHM = "HS256"


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    # 生成token
    :param subject: 保存到token的值
    :param expires_delta: 过期时间
    :return:
    """
    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解析验证
def check_jwt_token(
        token: Optional[str] = Header(None)
) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 担任也可以用 Header(None, alias="Authentication") 或者 alias="X-token"
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        # 抛出自定义异常， 然后捕获统一响应
        print("access token fail")
        # raise custom_exc.TokenAuthError(err_desc="access token fail")
