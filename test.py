LOCATION_LIST = [
    'audi north austin',
    'audi south austin',
    'bmw north austin',
    'austin porsche'
]


def test_adding_locations(location_list=None):
    if not location_list:
        location_list = LOCATION_LIST

    import main as m
    from gmbLocation import GmbLocation as gmbL

    job = gmbL()
    local_obj = job.readFile()

    for loc in location_list:
        print(loc)
        local_obj = m.updateLocalObject(loc, local_obj)

    job.addLocation(local_obj)
    return
