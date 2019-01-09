from flask import jsonify

def infos(source):
    return {
        'name': source.name,
        'channel': source.channel,
        'status': source.status
    }

# Views

def many(*sources):
    rv = []
    for source in sources:
        rv.append(infos(source))
    return jsonify(rv)

def one(source):
    return jsonify(infos(source))
