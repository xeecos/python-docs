# -*- coding: utf-8 -*

from setuptools import setup
setup(
    name='makeblock',
    version='0.0.58',
    author='makeblock',
    author_email='flashindream@gmail.com',
    url='https://makeblock.com',
    description=u'libraries for makeblock electron boards',
    packages=['makeblock','makeblock.Protocol','makeblock.SerialPort','makeblock.mBuild','makeblock.mCore','makeblock.MeAuriga','makeblock.MegaPi','makeblock.MegaPiPro','makeblock.MeOrion','makeblock.Neuron'],
    py_modules=['makeblock.Protocol.Protocol','makeblock.Protocol.PackData','makeblock.MeAuriga.modules','makeblock.mBuild.modules'],
    install_requires=['pyserial']
)