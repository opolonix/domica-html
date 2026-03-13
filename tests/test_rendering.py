import sys
import unittest


sys.path.insert(0, "src")

from domica_html import div, html, img, line, script, style, style_item
from domica_html.inctement import inc
from domica_html.node import item_context, node_container


class RenderingTests(unittest.TestCase):
    def tearDown(self):
        item_context.set(None)
        inc.context._indent.clear()
        inc.context._char.clear()
        inc.context._is_set = False

    def test_basic_document_render(self):
        doc = html()

        with doc:
            div("hello world")

        expected = "\n<html>\n    <div>\n        hello world\n    </div>\n</html>"
        self.assertEqual(doc.render(), expected)

    def test_attribute_values_are_html_escaped(self):
        rendered = div("x", title='a&b"<c>\'').render()
        self.assertIn('title="a&amp;b&quot;&lt;c&gt;&#x27;"', rendered)

    def test_open_tags_do_not_render_closing_tag(self):
        rendered = img(src="logo.svg", alt='logo & "icon"').render()
        self.assertEqual(rendered, '\n<img src="logo.svg" alt="logo &amp; &quot;icon&quot;">')

    def test_style_item_renders_css_block(self):
        rendered = style(style_item(".card", color="red", font_size="14px")).render()
        expected = (
            "\n<style>\n"
            "    .card {\n"
            "        color: red;\n"
            "        font-size: 14px;\n"
            "    }\n"
            "</style>"
        )
        self.assertEqual(rendered, expected)

    def test_line_uses_current_indentation(self):
        with script() as tag:
            line("const x = 1;")

        expected = "\n<script>\n    const x = 1;\n</script>"
        self.assertEqual(tag.render(), expected)

    def test_context_stack_is_created_and_cleared(self):
        self.assertIsNone(item_context.get())

        container = node_container()
        with container:
            stack = item_context.get()
            self.assertIsInstance(stack, list)
            self.assertEqual(stack[-1], container)

        self.assertIsNone(item_context.get())

    def test_anchor_auto_attaches_to_current_parent(self):
        parent = node_container()

        with parent:
            child = node_container(anchor=True)

        self.assertIs(child.parent, parent)
        self.assertEqual(parent.children, [child])

    def test_unpin_from_parent_returns_previous_parent(self):
        parent = node_container()
        child = node_container()
        parent.add_child(child)

        old_parent = child.unpin_from_parent()

        self.assertIs(old_parent, parent)
        self.assertIsNone(child.parent)
        self.assertEqual(parent.children, [])


if __name__ == "__main__":
    unittest.main()
