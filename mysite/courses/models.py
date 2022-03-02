from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(BaseModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.user.username}'


class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField()

    @property
    def review_avg(self):
        if not self.review_set.all():
            return 0
        review_avg = self.review_set.aggregate(
            review_avg=models.Avg("score"))["review_avg"]
        return review_avg

    @property
    def review_count(self):
        if not self.review_set.all():
            return 0
        review_count = self.review_set.count()
        return review_count

    def __str__(self) -> str:
        return f'{self.title}'


class Review(BaseModel):
    SCORE_CHOICES = (
        (5, "5"),
        (4, "4"),
        (3, "3"),
        (2, "2"),
        (1, "1"),
    )

    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField(choices=SCORE_CHOICES)

    def __str__(self) -> str:
        return f'{self.score}'
