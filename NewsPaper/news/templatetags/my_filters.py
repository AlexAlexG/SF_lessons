from django import template

register = template.Library()

@register.filter()
def bad_language(text:str):
   DIC_WORDS = [
      'редиска',
      'козел',
      'свинья',
      'all',
      'mars',
      'Редиска',
      'Козел',
      'Свинья',
      'All',
      'Mars',
   ]
   # text = text.translate({ord('.'): None})
   # text_s = text.split()
   # text_new = ''
   # for word in text_s:
   #    if isinstance(word,str):
   #       new_word = word
   #       if word.lower() in DIC_WORDS:
   #          new_word = word[0]+'*'*(len(word)-1)
   #       text_new+=new_word+' '
   #    else:
   #       print('Error! Check your filter!')
   # text_new.strip()
   for word in DIC_WORDS:
      if word in text:
            text = text.replace(word, word[0]+'*'*(len(word)-1))
   return text