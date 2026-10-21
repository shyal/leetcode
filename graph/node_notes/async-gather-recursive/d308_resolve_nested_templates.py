# REFERENCE: d308 Resolve Nested Templates
class Solution:
    async def mustachify(self, template, get_data):
        parts = re.split(r"\{\{(.*?)\}\}", template)

        async def fill(key):
            return await self.mustachify(await get_data(key), get_data)

        parts[1::2] = await asyncio.gather(*map(fill, parts[1::2]))
        return "".join(parts)
