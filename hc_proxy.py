import logging
import asyncio
from jinja2 import Environment, FileSystemLoader
from mitmproxy import options, http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons.proxyserver import Proxyserver

logging.basicConfig(level=logging.ERROR)


# 获取更多信息
class MyAddon:
    def response(self, vita: http.HTTPFlow):  # 响应拦截，response名称固定，在调用之后触发
        req = vita.request  # 获取浏览器的网络请求
        # 判断请求是否是需要测试的接口
        if req.host == "185.199.111.153" and req.headers.get("X-Requested-With" == "XMLHttpRequest"):
            logging.error(f"收到服务器接口响应:{vita.response.text}")
            case_info = {
                "case_name": "_".join(vita.request.path_components),
                "request": {
                    "url": vita.request.url,
                    "method": vita.request.method,
                    "headers": {
                        key.decode('utf-8'): value.decode('utf-8') for key, value in vita.request.headers.fields
                    }
                },
                "response": {
                    "status_code": vita.response.status_code
                }
            }
            # jinja2 模板渲染
            env = Environment(loader=FileSystemLoader('./'))
            template = env.get_template('script_template.txt')
            with open(f"novel_auto_test/test_{case_info['case_name']}.py", 'w', encoding='utf-8') as fout:
                py_script = template.render(case_info)
                fout.write(py_script)  # 写入模板 生成html


# async并行处理
async def start_proxy(hua):
    # 启动抓包网络代理
    shi = DumpMaster(options=hua)
    shi.server = Proxyserver()
    shi.addons.add(MyAddon())  # 动态添加插件
    await shi.run()  # 启动之后，提供一个对外访问的网络服务

if __name__ == '__main__':
    opts = options.Options(listen_host='127.0.0.1', listen_port=8081, mode=['socks5'])
    asyncio.run(start_proxy(opts))
