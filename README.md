##  Aliquant Python Client

### 运行 samples
1. 需要 python 2.7 环境

2. 运行 python setup.py install

3. 打开aliquant/config.py文件, 将 appId, appSecret, endpoint 替换为获取到的值

4. 运行脚本即可，目前提供了两种运行方式：
4-1. 推荐模式，python runner.py samples/strategy_simple.py运行，用户在runner.py中配置回测起始、终止时间和时间粒度，在samples/strategy_simple.py中实现回测逻辑。
4-2. 代码片段模式，python samples/simple.py运行，回测起始、终止时间和时间粒度都在samples/simple.py中配置，回测逻辑也在其中实现。
