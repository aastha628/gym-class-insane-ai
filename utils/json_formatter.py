import json


def getJsonResponse(cur, many=False):
    row_headers = [x[0] for x in cur.description]
    json_data = []

    if many:
        result = cur.fetchall()
        if cur.rowcount == 0:
            return []
        for r in result:
            json_data.append(dict(zip(row_headers, r)))
    else:
        result = cur.fetchone()
        if cur.rowcount == 0:
            return None
        json_data = dict(zip(row_headers, result))
    return json_data
