from flask import abort, request, jsonify

def get_paginated_list(list_object, url, page, limit):
    # check if page exists
    results = list_object
    count = len(results)
    if(count < page):
        abort(404)
    # make response
    results_list = []
    for result in results:
        result_data = {}
        result_data['id'] = result.id
        result_data['name'] = result.name
        result_data['description'] = result.description
        results_list.append(result_data)
    obj = {}
    obj['page'] = page
    obj['limit'] = limit
    obj['count'] = count
    # make urls
    # make previous url
    if page == 1:
        obj['previous'] = ""
    else:
        page_copy = max(1, page - limit)
        limit_copy = page - 1
        obj['previous'] = url + '?page=%d&limit=%d' % (page_copy, limit_copy)
    # make next url
    if page + limit > count:
        obj['next'] = ""
    else:
        page_copy = page + limit
        obj['next'] = url + '?page=%d&limit=%d' % (page_copy, limit)
    # extract result according to bounds
    obj['results'] = results_list[(page - 1) : (page - 1 + limit)]
    return jsonify(obj)
