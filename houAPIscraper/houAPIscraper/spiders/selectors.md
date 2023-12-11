# category name
texts = response.css('h2.label.heading.pull.left::text').getall()
clean_texts = [text.strip() for text in texts if text.strip()]

# class
homclass = response.css('a.label-text.homclass::text').getall()

# summary hom class
response.css('p.summary::text').getall()
 
# function name
response.css('div.collapsible.method.item.collapsed::attr(data-title)').getall()

# function summary

