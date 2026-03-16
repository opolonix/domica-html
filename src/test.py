from domica_html import html, div
import asyncio

doc = html()

with doc:
    div("hello world")

async def main():
    print(await doc.render())
asyncio.run(main())