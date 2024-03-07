from service.minMax import MinMax
from ui.ui import UI
from tests.tests import *

minmax = MinMax([[0 for _ in range(19)] for _ in range(19)])

ui = UI(minmax)
ui.start()
#unittest.main()