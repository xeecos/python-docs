#### 引用

```python
from makeblock.boards import Halocode
```

#### 初始化

```python
board=Halocode.create(device)
```

> 参数
* device:
```python
mlink #mlink服务
uart = SerialPort.create("COM3") #串口
BLE #蓝牙
```

#### 模块初始化

```python
button=Halocode.Button(board)
```

#### 获取数据

```python
button.is_pressed #最新缓存数据
button.request_pressed(callback) #主动请求数据，def callback(value)
```

#### 示例
```python
from time import sleep

from makeblock import SerialPort
from makeblock.boards import Halocode

if __name__ == '__main__':
    board = Halocode.create(SerialPort.create("/dev/cu.wchusbserial1410")) #光环板
    button = Halocode.Button(board) #板载按钮
    halo = Halocode.Halo(board) #板载RGB灯
    i = 0
    dir = 3
    while True:
        if button.is_pressed==1:
            i += dir
            if i>100:
                i = 100
                dir = -3
            if i<0:
                i=0
                dir = 3
            halo.set_colors(i,i,i)
        sleep(0.04)
```