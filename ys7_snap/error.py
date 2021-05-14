# 萤石云response错误代码表

ERROR_YS7_RESPONSE_CODE = {
    "200": "操作成功-请求成功",
    "201": "Created",
    "401": "Unauthorized",
    "402": "Forbidden",
    "403": "Forbidden",
    "404": "用户不存在",
    "10001": "参数错误-参数为空或格式不正确",
    "10002": "accessToken异常或过期-重新获取accessToken",
    "10005": "appKey异常-appKey被冻结",
    "10017": "appKey不存在-确认appKey是否正确",
    "10030": "appkey和appSecret不匹配",
    "20002": "设备不存在",
    "20006": "网络异常-检查设备网络状况，稍后再试",
    "20007": "设备不在线-检查设备是否在线",
    "20008": "设备响应超时-操作过于频繁，稍后再试",
    "20014": "deviceSerial不合法",
    "20018": "该用户不拥有该设备-检查设备是否属于当前账户",
    "20032": "该用户下通道不存在-该用户下通道不存在",
    "49999": "数据异常-接口调用异常",
    "60000": "设备不支持云台控制",
    "60001": "用户无云台控制权限",
    "60002": "设备云台旋转达到上限位",
    "60003": "设备云台旋转达到下限位",
    "60004": "设备云台旋转达到左限位",
    "60005": "设备云台旋转达到右限位",
    "60006": "云台当前操作失败-稍候再试",
    "60007": "预置点个数超过最大值",
    "60008": "C6预置点个数达到上限，无法添加-C6预置点最大限制个数为12",
    "60009": "正在调用预置点",
    "60010": "该预置点已经是当前位置",
    "60011": "预置点不存在",
    "60017": "设备抓图失败-设备返回失败",
    "60020": "不支持该命令-确认设备是否支持该操作"
}


def get_err_msg(err_code: str):
    return ERROR_YS7_RESPONSE_CODE.get(err_code, "未知错误")


class AccessTokenError(Exception):
    """获取access token error"""
    pass


class CaptureError(Exception):
    """抓拍 error"""
    pass


class FileStoreError(Exception):
    pass