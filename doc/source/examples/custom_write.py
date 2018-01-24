#!/usr/bin/env python3
from caproto.curio.high_level_server import pvproperty, PVGroupBase
import pathlib


class CustomWrite(PVGroupBase):
    """
    When a PV is written to, write the new value into a file as a string.
    """
    DIRECTORY = pathlib.Path('/tmp')

    async def my_write(self, instance, value):
        # Compose the filename based on whichever PV this is.
        pv_name = instance.pvspec.attr  # 'A' or 'B', for this IOC
        with open(self.DIRECTORY / pv_name, 'w') as f:
            f.write(str(value))
        return value

    A = pvproperty(put=my_write, value=[0])
    B = pvproperty(put=my_write, value=[0])


if __name__ == '__main__':
    # usage: custom_write.py <PREFIX>
    import sys
    import curio
    from caproto.curio.server import start_server

    ioc = CustomWrite(prefix=sys.argv[1])
    print('PVs:', list(ioc.pvdb))
    curio.run(start_server(ioc.pvdb))
