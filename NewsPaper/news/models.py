from django.db import models
from datetime import *
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse

article='AR'
news='NE'
TYPE=[
    (article, 'Статья'),
    (news, 'Новости')
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating= Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating')*3, 0))
        author_comment_rating=Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))
        self.user_rating = author_posts_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] + author_post_comment_rating['comments_rating_sum']
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=264, unique=True)



class Post(models.Model):
    author = models.ForeignKey(Author, default=1, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TYPE)
    time_in= models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=264)
    text = models.TextField()
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text[:124]
        if len(self.text) > 124:
            text += '...'
        return text

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    text_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



