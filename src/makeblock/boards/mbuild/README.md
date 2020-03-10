#### 引用

```python
from makeblock.boards import mBuild
```

#### 初始化

```python
board=mBuild.create(device)
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
ultrasonic=mBuild.Ultrasonic(board, index, mode)
```

>参数
* index：模块序号，1～255
* mode：数据采集模式，默认变化上报
```python
mBuild.MODE_REQUEST   #请求模式
mBuild.MODE_CHANGE    #变化上报模式
mBuild.MODE_PERIOD    #周期上报模式
```

#### 获取数据

```python
ultrasonic.distance #最新缓存数据
ultrasonic.request_distance(callback) #主动请求数据
ultrasonic.on_change(callback) #数据变化时回调
```

#### 示例
```python
from time import sleep

from makeblock import SerialPort
from makeblock.boards import mBuild,Halocode

if __name__ == '__main__':
    uart = SerialPort.create("COM3") #串口连接
    halocode = Halocode.create(uart) #mBuild模块接在光环板上
    mbuild = mBuild.create(uart) #mBuild链
    ultrasonic = mBuild.Ultrasonic(mbuild,1) #超声波模块
    servo = mBuild.Servo(mbuild,2) #舵机模块
    while True:
        servo.set_angle(ultrasonic.distance/300*180)
        sleep(0.1)
```