from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    # full_name = models.CharField(max_length = 255)
    ratingAuthor = models.SmallIntegerField(default = 0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        # суммарный рейтинг всех комментариев  к статьям автора.
        cpRat = sum(Comment.objects.filter(
            commentPost__in=Post.objects.filter(author=self)).values_list('rating', flat=True)
                                            )
        self.ratingAuthor = pRat*3 + cRat + cpRat
        self.save()

    def __str__(self):
        return self.authorUser
    class Meta:
        verbose_name= 'Автор'
        verbose_name_plural='Авторы'
        ordering=['authorUser']

class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.name_category
    class Meta:
        verbose_name= 'Категория'
        verbose_name_plural='Категории'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)

    dateCreation = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255)
    text = models.TextField()
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating+= 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
	    return self.text[0:123]+'...'

    def __str__(self):
        return f'{self.title}'
    class Meta:
        verbose_name= 'Новость'
        verbose_name_plural='Новости'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete = models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.postThrough

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text
    class Meta:
        verbose_name= 'Комментарий'
        verbose_name_plural='Комментарии'