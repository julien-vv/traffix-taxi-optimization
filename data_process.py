from imports import * 


# Sort original data
def get_latitude(dt):
    return float(dt.split(',')[1])
def get_longitude(dt):
    return float(dt.split(',')[0])
