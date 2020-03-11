Preparation
============

1. compile and upload the firmware of board to your board from |location_link|

.. |location_link| raw:: html

   <a href="https://github.com/Makeblock-official/Makeblock-Libraries/tree/master/examples" target="_blank">Github</a>

2. install package from pypi
    >>> pip3 install pyserial makeblock


.. toctree::
   :caption: Quickstart
   :maxdepth: 2

   preparation

.. autosummary::

    makeblock.boards.mcore

.. toctree::
    :hidden:
    :maxdepth: 3
    :caption: Makeblock Controller Boards

    makeblock.boards.mcore
    makeblock.boards.meorion
    makeblock.boards.meauriga
    makeblock.boards.megapi
    makeblock.boards.megapipro
    makeblock.boards.halocode
    makeblock.boards.mbuild
    makeblock.boards.codey
    makeblock.boards.neuron

.. toctree::
    :hidden:
    :caption: Utilities

    makeblock.SerialPort
