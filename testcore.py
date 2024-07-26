import xToolkit
import requests
import pytest
import os
'''
all_file = xToolkit.xfile.read("test.xlsx").excel_to_dict(sheet=0)
print(all_file)


@pytest.mark.parametrize("case", all_file)
def test_case_exec(case):
    tex = requests.request(
        url=case["接口url"],
        method=case["请求方式"],
        params=case["url参数"]
    )
    print("实际响应内容：", tex.text)
    assert case["预期状态码"] == tex.status_code, "测试不通过"
'''

if __name__ == '__main__':
    pytest.main(['--clean-alluredir', '--alluredir=-allure-results'])
    os.system(r"allure generate -c -o 测试报告")
