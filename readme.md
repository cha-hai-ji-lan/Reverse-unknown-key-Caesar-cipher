# 逆向未知密钥恺撒密码

---

版本 ： 1.0

<u>**python版本：3.12**</u>

最低要求：<u>**python 3.6**</u>

**模块版本**

>`translate` : <u>3.6.1</u>
>
>`pycnchant` : <u>3.2.2</u>

**说明：**

- 目前可选择**加密**/**解密**两个功能

- 选择后可输入**待加密文本**/**已加密文本**的<u>地址</u>或直接输入文本

- 若文本采取路径输入后然需要输入最终文本保存路径（绝对路径）

- 破译后可选择是否将原文翻译为汉语

  ​

**2.0版本预期：**

- 基于恺撒加密逻辑新增汉语文本**加密**/**解密**
- 自识别汉语/英语  加密  解密
- 增加默认文件保存路径，解放输入文件目录保存路径输入压力（保留自定义文件路径保存）
- 破译前增加定向密钥接收功能，在知道密钥的情况下降低破译破译时间
- 优化边界检测，一次破译失败后智能提取特征边界进行多轮破译降低恺撒密文破译失败概率

