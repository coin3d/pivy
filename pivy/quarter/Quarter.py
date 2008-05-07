from pivy import coin

from SensorManager import SensorManager

initialized = False


class Quarter:
    def __init__(self):
        global initialized
        assert(not initialized)
        coin.SoDB.init()
        coin.SoNodeKit.init()
        # FIXME jkg: do this?
        #coin.SoBaseKit.setSearchingChildren(coin.TRUE) # we always want to search under node kits
        # FIXME jkg: waiting for wrapper?
        #coin.SoInteractoin.init()

        self.sensormanager = SensorManager()
