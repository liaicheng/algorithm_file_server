## 流程
* 获取token
* 获取最新的需要处理的files列表
* 获取file（files）
* 接收file result

## 重要问题
* token有效性，安全性保障
* file处理的精确一次
 * 查看文件是否就位
 * 获取就位文件后，文件状态为：preprocess
 * 文件被处理后，成功状态是processed，失败为failed（有效期是两天）


* 用户数据处理流跟踪
 * 创建（文件就位）
 * 文件处理中（被获取）
 * 文件处理结束（异常或者成功）
 * 流程结束（发送给用户处理结果）
 