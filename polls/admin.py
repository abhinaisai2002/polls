from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Poll)
admin.site.register(PollsOptions)
admin.site.register(CommentBy)
admin.site.register(VotedBy)
