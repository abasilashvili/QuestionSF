from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_author = Post.objects.filter(author=self)
        posts_rating = sum(post.rating * 3 for post in posts_author)
        comments_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        post_comments_rating = sum(comment.rating for post in posts_author
                                   for comment in Comment.objects.filter(post=post))

        self.rating = posts_rating + comments_rating + post_comments_rating
        self.save()

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    objects = None
    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPES, default=NEWS)
    creation_date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + "..."

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.post_type == self.NEWS:
            return reverse('news_detail', args=[str(self.id)])
        elif self.post_type == self.ARTICLE:
            return reverse('article_detail', args=[str(self.id)])
        else:
            return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_category")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.category.title}"


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{str(self.user)} - {self.post.title}"


