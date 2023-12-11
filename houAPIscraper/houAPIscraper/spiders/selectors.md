# site
https://www.sidefx.com/docs/houdini/hom/hou/index.html
https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html

# category name
texts = response.css('h2.label.heading.pull.left::text').getall()
clean_texts = [text.strip() for text in texts if text.strip()]

# hom class
homclass = response.css('a.label-text.homclass::text').getall()

# summary hom class
response.css('p.summary::text').getall()
 
# data title
response.css('div.collapsible.method.item.collapsed::attr(data-title)').getall()
