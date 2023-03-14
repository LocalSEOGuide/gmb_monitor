import main as m
from gmbLocation import GmbLocation as gmbL

def adding_locations(location_list=None):
    if not location_list:
        location_list = LOCATION_LIST
    job = gmbL()
    local_obj = job.readFile()
    local_obj = m.updateLocations(LOCATION_LIST, local_obj)
    job.addLocation(local_obj)
