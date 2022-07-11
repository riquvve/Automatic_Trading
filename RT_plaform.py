import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import datetime
import math

fig = plt.figure()
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(6,6)