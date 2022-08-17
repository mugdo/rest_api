from django.db import models
from treebeard.mp_tree import MP_Node
from django_currentuser.db.models import CurrentUserField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import timedelta, datetime
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.contrib.auth.models import User

from faculty.models.instructor_model import Instructor, InstructorActivity, RATTING, COMMENT
from authenticate.models import UserInformation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from mixin.common_task import SlugGeneratorMixin
from notification.models import Notification, NotificationGroup, REPLY_COMMENT, REPLY_COMMENT_GROUP_NAME
from notification.utils import channel_group_send_data

BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3
COURSE_LEVEL = (
    (BEGINNER, 'Beginner'),
    (INTERMEDIATE, 'Intermediate'),
    (EXPERT, 'Expert')
)

POPULAR = 1
TRENDY = 2
NEW = 3
TRENDY_HIGH_DEMANDABLE = 4
COURSE_ACTIVITIES = (
    (POPULAR, 'Popular'),
    (TRENDY, 'Trendy'),
    (NEW, 'New'),
    (TRENDY_HIGH_DEMANDABLE, 'Trendy High Demand')
)

STORY = 1
REVIEW = 2

STUDENT = 1
INSTRUCTOR = 2

ANSWER_TYPE = (
    (STORY, 'Story'),
    (REVIEW, 'Review')
)
ANSWER_BY = (
    (STUDENT, 'Student'),
    (INSTRUCTOR, 'Instructor')
)

TESTIMONIAL_TYPE = (
    (STORY, 'Story'),
    (REVIEW, 'Review')
)

RESOURCE_FILE = 1
RESOURCE_LINK = 2

RESOURCE_TYPE = (
    (RESOURCE_FILE, 'File'),
    (RESOURCE_LINK, 'Link')
)

PERCENT = 1
AMOUNT = 2
DISCOUNT_TYPE = (
    (PERCENT, 'Percent'),
    (AMOUNT, 'Amount'))

CONTENT_LESSON = 1
CONTENT_QUIZ = 2

CONTENT_TYPE = (
    (CONTENT_LESSON, 'Lesson'),
    (CONTENT_QUIZ, 'Quiz')
)
COMMISSION_TYPE_CHOICES = (
    (PERCENT, 'Percent'),
    (AMOUNT, 'Amount')
)

SINGLE_ANSWER = 1
MULTIPLE_ANSWER = 2
QUIZ_QUESTION_TYPE = (
    (SINGLE_ANSWER, 'Single Answer'),
    (MULTIPLE_ANSWER, 'Multiple Answer')
)

PENDING = 1
APPROVED = 2
REJECTED = 3
ARCHIEVED = 4
DRAFT = 5
UNPUBLISHED = 6

PAID = 1
FREE = 2
SPECIAL_OFFER = 3

COURSE_TYPE = (
    (PAID, 'Paid'),
    (FREE, 'Free'),
    (SPECIAL_OFFER, 'Special Offer')
)

COURSE_STATUS = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
    (ARCHIEVED, 'Archived'),
    (DRAFT, 'Draft'),
    (UNPUBLISHED, 'Unpublished')
)


class Category(MPTTModel):
    def get_category_photo_path(self, filename):
        return "images/{category}/{filename}".format(category=self.name, filename=filename)

    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True)
    description = models.TextField()
    video_id = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    priority = models.IntegerField(default=0)
    unique_code = models.CharField(null= True, max_length= 15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="category_created", on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, related_name="category_updated", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Category)
def category_slug_generate(sender, instance, created, **kwargs):
    if created:
        if instance.slug is None:
            slug_object = SlugGeneratorMixin()
            slug = slug_object.unique_slug_generator(instance)
            instance.slug = slug
            instance.save()


def course_image(instance, filename):
    return '/'.join(['course', instance.name, filename])


class ApproveCourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=APPROVED)


class Course(models.Model):

    def __init__(self, *args, **kwargs):
        self.is_api_request = None
        super(Course, self).__init__(*args, **kwargs)

    instructor = models.ForeignKey(Instructor, null=True, related_name='courses', on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name="courses", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=COURSE_STATUS, blank=True, null=True, default=5)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)
    name = models.CharField(max_length=200)
    course_activities = models.PositiveSmallIntegerField(choices=COURSE_ACTIVITIES, null=True)
    highlighted_text = models.TextField(null=True)
    avg_rating = models.PositiveSmallIntegerField(default=5)
    total_review = models.IntegerField(default=0)
    image = models.ImageField(upload_to=course_image, height_field=None, width_field=None, max_length=None)
    price = models.IntegerField(default=0, blank=True)
    discount_price = models.IntegerField(blank=True, default=0)
    course_level = models.PositiveSmallIntegerField(choices=COURSE_LEVEL, null=True)
    is_balance_purchase = models.BooleanField(default=False)
    course_type = models.PositiveSmallIntegerField(choices=COURSE_TYPE, null=True)
    course_duration_in_sec = models.IntegerField(default=0)  # auto fill by signals
    tags = models.TextField(null=True)
    is_published= models.BooleanField(default= False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="courses_create", on_delete=models.SET_NULL, null=True)

    objects = models.Manager()  # The default manager.
    approve_courses = ApproveCourseManager()

    def __str__(self):
        return self.name


class CourseCommission(models.Model):
    course = models.OneToOneField(Course, related_name='commission', on_delete=models.CASCADE)
    commission_type = models.IntegerField(choices=COMMISSION_TYPE_CHOICES, default=PERCENT)
    amount = models.FloatField(default= 0)

    def __str__(self):
        return self.course.name


class CourseCurriculum(models.Model):
    course = models.OneToOneField(Course, related_name='course_curriculum', on_delete=models.CASCADE)
    total_topic = models.IntegerField(default=0)
    total_lesson = models.IntegerField(default=0)
    total_video = models.IntegerField(default=0)
    total_quiz = models.IntegerField(default=0)

    def __str__(self):
        return self.course.name


class CourseLandingInformation(models.Model):
    course = models.OneToOneField(Course, related_name='landing_information', on_delete=models.CASCADE)
    specification = models.TextField(null=True)
    description = models.TextField(null=True)
    what_you_will_learn = models.TextField(null=True)
    certificate_value = models.TextField(null=True)
    career_upper_text = models.TextField(null=True)
    career_bullet_text = models.TextField(null=True)
    for_whom_upper_text = models.TextField(null=True)
    for_whom_bullet_text = models.TextField(null=True)
    course_requirement_text = models.TextField(null=True)
    course_requirement_bullet_text = models.TextField(null=True)
    how_to_join_text = models.TextField(null=True)
    how_to_join_bullet_text = models.TextField(null=True)

    def __str__(self):
        return self.course.name


class CourseHelpToMarket(models.Model):
    course = models.OneToOneField(Course, related_name='course_help_to_market', on_delete=models.CASCADE)
    description = models.TextField(null=True)

    def __str__(self):
        return self.course.name


class HelpToMarketImage(models.Model):
    help_to_market = models.ForeignKey(Course, related_name='help_to_market_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/helptomarket/')


class SoftwareLearn(models.Model):
    course = models.OneToOneField(Course, related_name='software_learn', on_delete=models.CASCADE)
    description = models.TextField(null=True)

    def __str__(self):
        return self.course.name


class SoftwareLearnImage(models.Model):
    name = models.CharField(max_length=200)
    software_learn = models.ForeignKey(Course, related_name='software_learn_image',
                                       on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/softwarelearn/')

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.OneToOneField(Course, related_name='course_resource', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.course.name


class CourseResourceImage(models.Model):
    name = models.CharField(max_length=200)
    course_resource = models.ForeignKey(Course, related_name='course_resource_image',
                                        on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/course_resource/')

    def __str__(self):
        return self.name


class CourseTestimonial(models.Model):
    course = models.ForeignKey(Course, related_name="course_testimonials", on_delete=models.CASCADE)
    testimonial_type = models.PositiveSmallIntegerField(choices=TESTIMONIAL_TYPE)
    title = models.CharField(max_length=250)
    review_star = models.FloatField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='course/course_testimonial/')

    def __str__(self):
        return self.course.name


@receiver(post_save, sender=Course)
def course_slug_generate(sender, instance, created, **kwargs):
    if created:
        CourseLandingInformation.objects.create(course=instance)
        CourseCurriculum.objects.create(course=instance)
        CourseHelpToMarket.objects.create(course=instance)
        SoftwareLearn.objects.create(course=instance)
        CourseResource.objects.create(course=instance)
        CourseCommission.objects.create(course=instance)
        if instance.slug is None:
            slug_object = SlugGeneratorMixin()
            slug = slug_object.unique_slug_generator(instance)
            instance.slug = slug
            instance.save()


class CourseSuccessVideo(models.Model):
    course = models.ForeignKey(Course, related_name="course_success_video", on_delete=models.CASCADE)
    video_id = models.CharField(max_length=30)

    def __str__(self):
        return self.course.name


class CourseContent(models.Model):
    content_section = models.PositiveSmallIntegerField(choices=CONTENT_TYPE)
    order = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, related_name="single_contents", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.get_content_section_display() +  '--' +str(self.content_type.app_label)


class Topic(models.Model):
    course = models.ForeignKey(Course, related_name='topics', null=True, on_delete=models.CASCADE)
    serial = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=250)
    total_sec = models.IntegerField(default=0)
    content = models.ManyToManyField(CourseContent, related_name="topics")

    @property
    def total_content(self):
        return self.content.all().count()

    def __str__(self):
        return self.course.name + '--' + str(self.name)


@receiver(post_save, sender=Topic)
def update_topic_count(sender, instance, created, **kwargs):
    if created:
        curriculum = instance.course.course_curriculum
        curriculum.total_topic += 1
        curriculum.save()


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE, null=True)
    topic_wise_serial = models.IntegerField(default=0)
    lesson_serial = models.IntegerField(default=0)
    name = models.CharField(max_length=250)
    lesson_duration_in_sec = models.IntegerField(default=0)
    video_id = models.CharField(max_length=250, null=True)
    single_content = GenericRelation(CourseContent)
    depended_quiz_for_unlock = models.ForeignKey('course.Quiz', related_name="lesson_unlock", on_delete=models.CASCADE,
                                                 null=True, blank=True)
    is_default_unlock = models.BooleanField(default=False)

    @property
    def attachment_count(self):
        return self.lesson_resources.all().count()

    def __str__(self):
        return self.topic.course.name + '--' + str(self.name)


def update_course_second(instance, second):
    topic = instance.topic
    topic.total_sec += second
    topic.course.course_duration_in_sec += second
    topic.save()
    topic.course.save()


@receiver(post_save, sender=Lesson)
def set_default_quiz(sender, instance, created, **kwargs):
    if created:
        curriculum = instance.topic.course.course_curriculum
        curriculum.total_lesson += 1
        curriculum.total_video += 1
        curriculum.save()

        course_content = CourseContent.objects.filter(topics__course=instance.topic.course).order_by('-id')
        last_lesson = Lesson.objects.filter(topic=instance.topic).order_by('-id')
        instance.topic_wise_serial = last_lesson.count()
        instance.lesson_serial = course_content.count() + 1
        instance.save()

        duration_track= LessonDurationTrack.objects.filter(created_at__lte=datetime.now() - timedelta(days=10))
        if duration_track.exists():
            duration_track.delete()

        sec = instance.lesson_duration_in_sec
        if sec is not None:
            update_course_second(instance, sec)


class VideoQuizQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_quiz_questions', on_delete=models.CASCADE)
    question_type = models.PositiveSmallIntegerField(choices=QUIZ_QUESTION_TYPE, null=True)
    show_second = models.CharField(max_length=10)
    label = models.CharField(max_length=250)

    def __str__(self):
        return self.lesson.name + '---' + self.label


class VideoQuizAnswer(models.Model):
    question = models.ForeignKey(VideoQuizQuestion, related_name='video_quiz_answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_right_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text + '---'+ str(self.question.label)


class LessonDurationTrack(models.Model):
    video_uri = models.CharField(max_length=50)
    lesson_duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_uri


class Quiz(models.Model):
    topic = models.ForeignKey(Topic, related_name="quizs", on_delete=models.CASCADE, null=True)
    topic_wise_serial = models.IntegerField(default=0)
    lesson_serial = models.IntegerField(default=0)
    lesson = models.ManyToManyField(Lesson)
    name = models.CharField(max_length=250)
    total_question = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    right_percent_need = models.IntegerField(default=6)
    num_of_random_question = models.IntegerField(default=10)
    single_content = GenericRelation(CourseContent)

    def __str__(self):
        return self.name + ' topic: ' + str(self.topic.name)


@receiver(post_save, sender=Quiz)
def update_quiz_count(sender, instance, created, **kwargs):
    if created:
        curriculum = instance.topic.course.course_curriculum
        curriculum.total_lesson += 1
        curriculum.total_quiz += 1
        curriculum.save()

        course_content = CourseContent.objects.filter(topics__course=instance.topic.course).order_by('-id')
        last_quiz = Quiz.objects.filter(topic=instance.topic).order_by('-id')
        instance.topic_wise_serial = last_quiz.count()
        instance.lesson_serial = course_content.count() + 1
        instance.save()


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_question', on_delete=models.CASCADE)
    question_type = models.PositiveSmallIntegerField(choices=QUIZ_QUESTION_TYPE, null=True)
    label = models.CharField(max_length=250)
    image = models.ImageField(upload_to='quiz/question/', null=True)

    def __str__(self):
        return self.label


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='quiz_answer', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_right_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class ReviewManager(models.Manager):
    def avg(self):
        if self.count() <= 0:
            return 0

        avg_total = 0
        for review in self.all().filter(is_approved=True):
            avg_total += review.rating
        return avg_total / self.count()


class Review(models.Model):
    student = models.ForeignKey('faculty.Student', related_name='student_reviews', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_reviews', on_delete=models.CASCADE)
    rating = models.FloatField(default=5)
    comment = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=False)
    objects = ReviewManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.student.full_name + '--'  + self.course.name


def content_file_name(instance, filename):
    return '/'.join(['resource', instance.lesson.name, filename])


@receiver(post_save, sender=Review)
def activity_create_for_review(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        activity = InstructorActivity()
        activity.instructor = course.instructor
        activity.activity_type = RATTING
        activity.course_name = course.name
        activity.student = instance.student
        activity.ratting = instance.rating
        activity.save()


class LessonResource(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_resources', on_delete=models.CASCADE, null=True)
    resource_type = models.PositiveSmallIntegerField(choices=RESOURCE_TYPE)
    file_size = models.CharField(max_length=50, null=True)
    uploaded_file = models.FileField(upload_to=content_file_name, null=True)
    link = models.TextField(null=True)

    def __str__(self):
        return self.lesson.name


class CourseAnnouncement(models.Model):
    course = models.ForeignKey(Course, related_name='announcements', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True, null=True)
    created_by = CurrentUserField()

    def __str__(self):
        return self.course.name


class CourseQuestion(models.Model):
    course = models.ForeignKey(Course, related_name='course_questions', on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateField(auto_now_add=True, null=True)
    student = models.ForeignKey('faculty.Student', related_name="course_questions", on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)
    read_by_instructor = models.BooleanField(default=False)
    answered_by_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.course.name


@receiver(post_save, sender=CourseQuestion)
def activity_create_for_question(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        activity = InstructorActivity()
        activity.instructor = course.instructor
        activity.activity_type = COMMENT
        activity.course_name = course.name
        activity.student = instance.student
        activity.save()


class QuestionAnswer(models.Model):
    question = models.ForeignKey(CourseQuestion, related_name="question_answers", on_delete=models.CASCADE)
    answer = models.TextField()
    answer_by = models.PositiveSmallIntegerField(choices=ANSWER_BY)
    student = models.ForeignKey('faculty.Student', related_name="question_answer", on_delete=models.CASCADE, null=True,
                                blank=True)
    instructor = models.ForeignKey(Instructor, related_name="question_answer", on_delete=models.CASCADE, null=True,
                                   blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.question.question


@receiver(post_save, sender=QuestionAnswer)
def create_notification(sender, instance, created, **kwargs):
    if created:
        if instance.answer_by == STUDENT:
            student = instance.student
            group, created_obj = NotificationGroup.objects.get_or_create(
                group_name='{}_{}'.format(REPLY_COMMENT_GROUP_NAME, instance.question_id), group_type=REPLY_COMMENT
            )
            if created_obj:
                group.student.add(*[instance.question.student, instance.student])
            else:
                if instance.student not in group.student.all():
                    group.student.add(instance.student)

            notification = Notification()
            notification.user = student.user
            notification.author_name = student.full_name
            title = '{} কোর্সে একটি কমেন্ট করেছেন'.format(instance.question.course.name)
            notification.title = title
            profile_image = student.profile_image.url
            notification.image = profile_image
            notification.group = group
            notification.save()
            channel_group_send_data(group.group_name, '', profile_image, title, \
                                    notification.created_at)  # channel