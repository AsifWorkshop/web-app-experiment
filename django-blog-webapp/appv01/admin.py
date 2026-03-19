from django.contrib import admin
from .models import user, post, comment, reply,tagpostjunc,tag

admin.site.register(user)
admin.site.register(post)
admin.site.register(comment)
admin.site.register(reply)
admin.site.register(tagpostjunc)
admin.site.register(tag)