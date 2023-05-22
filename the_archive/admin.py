from django.contrib import admin

from .models import Location, Upload, Comment, Bookmark, Link, FileBookmark

admin.site.register(Location)
admin.site.register(Upload)
admin.site.register(Comment)
admin.site.register(Bookmark)
#admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(FileBookmark)
