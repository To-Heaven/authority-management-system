from django.conf import settings
from re import match

from rbac import models


def init_permission(user, request):
    """ 初始化用户权限数据包括权限数据和与权限相关的菜单数据
    Args:
        user: 当前登陆并验证成功的用户
        request: 当前请求对象
    Return:
        None
    """

    permissions = user.roles.values("permissions__url",
                                    "permissions__feature",
                                    "permissions__id",
                                    "permissions__group_menu",
                                    "permissions__group__menu__id",
                                    "permissions__group__menu__title")

    # 权限相关
    permission_dict = {"features": [], "urls": []}
    for item in permissions:
        permission_dict["features"].append(item["permissions__feature"])
        permission_dict["urls"].append(item["permissions__url"])
    request.session[settings.PERMISSION_DICT] = permission_dict

    # 菜单相关
    menu_list = []
    for item in permissions:
        temp = {}
        temp["id"] = item["permissions__id"]
        temp["url"] = item["permissions__url"]
        temp["feature"] = item["permissions__feature"]
        temp["group_menu"] = item["permissions__group_menu"]
        temp["menu_id"] = item["permissions__group__menu__id"]
        temp["menu_title"] = item["permissions__group__menu__title"]
        menu_list.append(temp)
    request.session[settings.MENU_LIST] = menu_list