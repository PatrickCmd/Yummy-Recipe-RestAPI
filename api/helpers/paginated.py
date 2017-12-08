from flask import abort, request

def get_paginated_list(list_object, url, start, limit):
    # check if page exists
    results = list_object
    count = len(results)
    if(count < start):
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make urls
    # make previous url
    if start == 1:
        obj['previous'] = ""
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ""
    else:
        start_copy = start + limit
        obj['next'] = url + '?start%d&limit=%d' % (start_copy, limit_copy)
    # extract result according to bounds
    obj['results'] = results[(start - 1) : (start - 1 + limit)]
    return obj
