# category name
texts = response.css('h2.label.heading.pull.left::text').getall()
clean_texts = [text.strip() for text in texts if text.strip()]