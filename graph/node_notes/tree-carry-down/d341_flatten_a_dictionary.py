# REFERENCE: d341 Flatten a Dictionary
class Solution:
    def flatten_dictionary(self, dictionary):
        flat = {}

        def walk(prefix, d):
            for key, value in d.items():
                path = prefix + "." + key if prefix and key else prefix or key
                if isinstance(value, dict):
                    walk(path, value)
                else:
                    flat[path] = value

        walk("", dictionary)
        return flat
