# 接口

`POST /api/run`：JSON中的csv文本，省略使用样例；或multipart字段file。最大5MB。

`POST /api/m1`至`POST /api/m7`：独立运行到指定模块，JSON结构同运行接口。

`GET /api/history`：历史批次。`POST /api/review`接收id、revision和decision（通过或退回）。`GET /api/evidence.csv`提供单一证据导出。

结构错误422，版本变化409，文件过大413；错误返回code与message。所有页面可从左侧七个模块入口访问。

`GET /api/runs/<id>`读取指定批次；页面与证据CSV通过run_id查询参数绑定批次，模块导航保留该参数。

JSON请求体必须是对象，数组、标量、null、损坏JSON及错误上传字段返回400，且不运行默认样例。

云区多区间：cloud_w/cloud_e按分号分隔并按下标配对（见docs/DATA-DICTIONARY.md），样例见sample_data/multi-cloud.csv。结构错误（空文件、表头损坏等）返回422且不落库，上一版候选批次保留；行级云区错误以CLOUD/COORD进入隔离面板，同一目录修正后重试用SHA256+规则版本去重，不新增批次。规则版本是批次身份的一部分：已签核的旧批次（manifest中带原rule_version）通过run_id按原契约重放，页面与证据CSV可同时核对当前多区间批次与旧批次原结果。
