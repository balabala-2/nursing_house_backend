from dao.config import session
from dao.table.user import *
from schemas.other import User_head_feature_info, User_head_image_info
import numpy as np

def add_user_head_feature(user_head_feature_info: User_head_feature_info):
    """添加用户头像特征数据128D

    Args:
        user_head_feature_info (User_head_feature_info): _description_

    Returns:
        _type_: _description_
    """
    try:
        user_head_feature = User_head_feature(**user_head_feature_info.dict())
        session.add(user_head_feature)
        session.commit()

        return 1, "添加成功"
    except Exception as e:
        return 0, f"添加失败: {e}" 

def add_user_head_img(user_head_image_info: User_head_image_info):
    """添加用户头像数据

    Args:
        user_head_image_info (User_head_image_info): _description_

    Returns:
        _type_: _description_
    """
    try:
        user_head_image = User_head_image(**user_head_image_info.dict())
        session.add(user_head_image)
        session.commit()

        return 1, "添加成功"
    except Exception as e:
        return 0, f"添加失败: {e}"

# TODO
def get_user_head_img(user_type, user_id):
    img = session.query(User_head_image).filter_by(user_id=user_id, user_type=user_type).all()[-1]
    return img.image

def get_head_feature():
    try:
        features = session.query(User_head_feature).all()
        user_types = []
        user_ids = []
        user_features = []
        for feature in features:
            user_types.append(feature.user_type)
            user_ids.append(feature.user_id)
            user_features.append(np.fromstring(feature.head_feature, dtype=np.float16))
        
        return 1, "查询成功", {'user_ids': user_ids, 'user_types': user_types, 'user_features': user_features}
    except Exception as e:
        print(e)
        return 0, "查询失败", None
        
