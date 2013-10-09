import collections

class Flattener():
    """object flattener"""
    def __init__(self, *args, **kwargs):
        self.max_array_length = kwargs.get('max_array_length')
        self.one_index = kwargs.get('one_index', False)
        self.delimiter = kwargs.get('delimiter', '.')
        self.columns = kwargs.get('columns', None)

    def _flatten(self, obj, prefix=[], key=None):
        items = []
        tokens = prefix[:]
        include_element = True

        if not key is None:
            tokens.append(key)
        if isinstance(obj, dict):
            for k, v in obj.items():
                items += self._flatten(v, tokens, k)
        elif isinstance(obj, list):
            for idx in range(self.max_array_length if self.max_array_length is not None else len(obj)):
                v = obj[idx] if idx<len(obj) else None
                items += self._flatten(v, tokens, str(idx+1) if self.one_index else str(idx))
        elif obj is not None:
            if include_element:
                items.append((tokens, obj))
        # if called from caller, chnage to a dict of k,v instead of array of k,v
#        if len(tokens)==0:
#            items = dict(items)
        return items

    def to_dict(self, obj):
        def gen_key(key_parts):
            return self.delimiter.join(key_parts)

        # [collections.OrderedDict(sorted(d.items(), key=lambda t: t[0])) for d in data]
        items = {gen_key(item[0]):item[1] for item in self._flatten(obj)}

        if self.columns is not None:
            items = {k:v for k, v in items.items() if k in self.columns }

        return items

#    def parseFilter(self, columns):
#        self.filter = {}
#        for entry in columns.split(','):
#            parts = entry.split(':')
#            print parts
#            info = { 'include' : True, 'array_length' : None }
#            if len(parts)>1:
#                info['array_length'] = int(parts[1])
#            self.filter[parts[0]] = info
#        print self.filter
