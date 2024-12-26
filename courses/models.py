from django.db import models

from users.models import User


LESSON_TYPE = (
    ("lesson", "Dars"),
    ("quiz", "Test"),
)

QUESTION_TYPE = (
    ("one_select", "Bitta javob tanlash"),
    ("many_select", "Ko'p javob tanlash"),
    ("writable", "Yoziladigan"),
    ("matchable", "Mos keladigan"),
)


class Question(models.Model):
    question = models.TextField()
    type = models.CharField(max_length=100, choices=QUESTION_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value_1 = models.TextField(null=True, blank=True)
    value_2 = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value_1
    

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, related_name="quiz_questions")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="images/courses")
    price = models.IntegerField()
    students = models.ManyToManyField(User, related_name="course_students", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def count_students(self):
        return self.students.count()
    

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=LESSON_TYPE)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.IntegerField(default=60)
    video = models.URLField(null=True, blank=True)
    source = models.FileField(upload_to="files/lessons", null=True, blank=True)
    previous = models.ForeignKey("self", related_name="previous_lesson", on_delete=models.SET_NULL, null=True, blank=True)
    next = models.ForeignKey("self", related_name="next_lesson", on_delete=models.SET_NULL, null=True, blank=True)
    finishers = models.ManyToManyField(User, related_name="lesson_finishers", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def is_quiz(self):
        return True if self.quiz else False
    
    def has_previous(self):
        return True if self.previous else False
    
    def has_next(self):
        return True if self.next else False
    
    def count_finishers(self):
        return self.finishers.count()
    
    def finishers_list(self):
        return self.finishers.all()
    
    def end_lesson(self, user: User):
        self.finishers.add(user)


