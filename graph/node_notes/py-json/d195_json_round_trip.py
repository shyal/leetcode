# REFERENCE: d195 JSON Round Trip
class Solution:
    def encode(self, obj):
        return json.dumps(obj, sort_keys=True)

    def decode(self, text):
        return json.loads(text)
