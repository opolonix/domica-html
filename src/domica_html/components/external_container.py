
from domica_html import node_container
from contextvars import ContextVar
from collections import defaultdict
from typing import Type

external_tags: ContextVar[dict[Type, list["external_container"]]] = ContextVar("external_tags", default=None)

class external_container(node_container):
    def __init__(self, *, anchor=False):
        super().__init__(anchor=anchor)
        if not anchor:
            tags = external_tags.get()
            if tags is None:
                tags = defaultdict(list)
                external_tags.set(tags)
            tags[self.__class__].append(self)

    async def render(self):
        tags = external_tags.get() or defaultdict(list)

        for child in tags[self.__class__]:
            if child is self: continue
            self.add_child(child)

        return await super().render()
    

class global_script(external_container): ...
class global_styles(external_container): ...
class global_head(external_container): ...