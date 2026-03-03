from typing import Optional, List, Protocol, TYPE_CHECKING

import contextvars
import inspect

item_context: contextvars.ContextVar[List["node_container"]] = contextvars.ContextVar("item_context", default=[])

if TYPE_CHECKING:
    class node_container_rotocol(Protocol):
        def add_child(self, child: "node") -> None: ...
        def remove_child(self, child: "node") -> None: ...


class node_base:
    @staticmethod
    def render_item(value) -> str:
        if isinstance(value, list | tuple):
            return "".join([node_base.render_item(v) for v in value])
        if isinstance(value, node):
            return value.render()
        if hasattr(value, "re_render") and callable((to_call := getattr(value, "re_render"))):
            return to_call()
        if callable(value):
            return value()
        return str(value)


    @staticmethod
    async def async_render_item(value): 
        if isinstance(value, list):
            return "".join([await node_base.async_render_item(v) for v in value])
        if isinstance(value, node):
            result = value.render()
            if inspect.isawaitable(result):
                return await result
            return result

        if hasattr(value, "re_render") and callable((to_call := getattr(value, "re_render"))):
            result = to_call()
            if inspect.isawaitable(result):
                return await result
            return result

        if callable(value):
            result = value()
            if inspect.isawaitable(result):
                return await result
            return result

        return str(value)



class node:
    def __init__(self, anchor: bool = False):
        self._parent: Optional["node_container_rotocol"] = None

        if anchor:
            parent = self.get_parent()
            if parent:
                parent.add_child(self)

    @property
    def parent(self) -> Optional["node_container_rotocol"]:
        return self._parent
    
    def value_sync(self, value):
        return node_base.render_item(value)

    async def value_async(self, value):
        return await node_base.async_render_item(value)

    @parent.setter
    def parent(self, value: Optional["node_container_rotocol"]):
        self._parent = value

    def get_parent(self) -> Optional["node_container_rotocol"]:
        stack = item_context.get()
        return stack[-1] if stack else None

    def unpin_from_parent(self) -> Optional["node_container_rotocol"]:
        if self._parent:
            self._parent.remove_child(self)
            old_parent = self._parent
            self._parent = None
            return old_parent
        return None

    def __enter__(self):
        stack = item_context.get()
        stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        stack = item_context.get()
        stack.pop(-1)
        return False

    def __str__(self):
        return self.value_sync(self.render())

    def render(self):
        return "<node/>"
    
    

class node_container(node):
    def __init__(self, anchor: bool = False):
        super().__init__(anchor)
        self.children: List[node] = []

    def add_child(self, child: node):
        child.unpin_from_parent()
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: node):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def render(self):
        return self.children