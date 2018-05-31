from django.db import models

#用户
class User(models.Model):
    email = models.CharField(max_length=254,primary_key=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#日志主档
class Logacn(models.Model):
    title=models.CharField(max_length=200)
    pub_date=models.DateTimeField()

    def __str__(self):
        return self.title

#日志明细档
class Logtxn(models.Model):
    logacn=models.ForeignKey(Logacn)
    content=models.TextField()

    def __str__(self):
        return self.content

#文章分类
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

#文章标签
class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

#博客文章
class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    created_time=models.DateTimeField()
    modified_time=models.DateTimeField()
    excerpt=models.CharField(max_length=200,blank=True)
    category=models.ForeignKey(Category)
    tags=models.ManyToManyField(Tag,blank=True)
    author=models.ForeignKey(User)
    #新增字段统计阅读量
    views=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])

    class Meta:
        ordering=['-created_time']

##博客评论
class Comment(models.Model):
    email=models.EmailField(max_length=255)
    text=models.TextField()
    created_time=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey('Post')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering=['-created_time']