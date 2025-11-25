from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password, check_password

class StudentAccount(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # 存加密後的密碼

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class Student(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)      # 課名不可重複
    code = models.CharField(max_length=10, unique=True)      # 課號不可重複
    teacher = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    final_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ['student', 'course']      # 同一學生同一課不可重複

    @property
    def average(self):
        return (self.midterm_score + self.final_score) / 2

    def __str__(self):
        return f"{self.student.name}－{self.course.name} 修課紀錄"
