# this file houses misc helper functions that don't fit in the other files.

# change the given float game clock to mm:ss
def floatToTimer(float):
    preDecimal = int(float)
    minutes = preDecimal//60
    seconds = preDecimal%60
    return "%02d:%02d" % (minutes,seconds)