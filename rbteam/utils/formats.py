def id_to_name(_id):
    return _id.replace('-', ' ').title()

def pop_keys(data, *args):
    poped_data = {}
    for key in args:
        value = data.pop(key, False)
        if value : poped_data[key] = value
    return poped_data

def get_prefixed_keys(dictionnary, prefix, lowercase=True, trim=True):
    """
    This function returns key/value pairs which the key starts with given prefix.

    Arguments:
        dictionnary (Mandatory) <dict>   :  the dictionnary to parse
        prefix      (Mandatory) <string> :  the prefix used for key matching
        pop                     <bool>   :  if set to True (False by default), the matching
                                            keys will be poped of the given dictionnary
        lowercase               <bool>   :  if set to True (default), all matching
                                            keys will be lowercased
        trim                    <bool>   :  if set to True (default), all matching
                                            keys name will have the given prefix trimed
    """
    matching = {}
    non_matching = {}
    for k, v in dictionnary.items():
        if not k.startswith(prefix):
            non_matching[k] = v
            continue
        if trim:
            key = k[len(prefix):]
        else:
            key = k
        if lowercase:
            key = key.lower()
        matching[key] = v
    return {'matching': matching, 'others': non_matching}
