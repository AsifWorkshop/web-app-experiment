from django.db import models
from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique':"A user with That Username Already Exists."
        }
    )
    created_at=models.DateTimeField(auto_now_add=True)
    attachment = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username

class post(models.Model):
    author=models.ForeignKey('user',on_delete=models.CASCADE,related_name='posts')
    title=models.TextField()
    content=models.TextField()
    likes_count=models.BigIntegerField(default=0)
    comments_count=models.BigIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    attachment=models.ImageField(upload_to='', blank=True, null=True)
    users_who_liked = models.ManyToManyField('user', related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

class comment(models.Model):
    post=models.ForeignKey('post',on_delete=models.CASCADE,related_name='comments')
    commentator=models.ForeignKey('user',on_delete=models.CASCADE)
    comment_content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.commentator.username} on {self.post.title[:20]}"
    
class reply(models.Model):
    comment=models.ForeignKey('comment',on_delete=models.CASCADE,related_name='replies')
    post=models.ForeignKey('post',on_delete=models.CASCADE)
    commentator=models.ForeignKey('user',on_delete=models.CASCADE)
    reply_content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.commentator.username}: {self.reply_content[:20]}..."
    class Meta:
        verbose_name_plural = "replies"

class tag(models.Model):
    name=models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.name

class tagpostjunc(models.Model):
    post=models.ForeignKey('post',on_delete=models.CASCADE,related_name="post_tag")
    tag=models.ForeignKey('tag',on_delete=models.CASCADE,related_name='tag_post')

    class Meta:
        unique_together = ('post', 'tag')
    def __str__(self):
        return f"{self.tag.name} on {self.post.title}"