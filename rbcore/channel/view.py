from flask import jsonify

def infos(channel):
    info = channel._document
    info['source'] = {
        'name': channel.source.name,
        'status': channel.source.status
    }
    info.pop('deleted')
    return info

# Views
def many(*channels):
    rv = []
    for channel in channels:
        rv.append(infos(channel))
    return jsonify(rv)

def one(channel):
    return jsonify(infos(channel))
