from django.db import models
from App_auth.models import *

# Create your models here.
podcastCategories = (
    ('Stories', 'Stories'),
    ('Education', 'Education'),
    ('Music', 'Music'),
    ('Coding', 'Coding'),
    ('Life & Goal', 'Life & Goal'),
    ('Business & Technology', 'Business & Technology'),
    ('Art & Culture', 'Art & Culture'),
    ('Science', 'Science'),
    ('Motivation', 'Motivation'),
    ('Health & Sports', 'Health & Sports'),
)


class PodcastModel(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='podcast_creator')
    title = models.CharField(max_length=800)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='podcast_images', blank=True, null=True)
    audio_file = models.FileField(upload_to='music/', blank=False, null=False)
    categories = models.CharField(max_length=30, blank=True, null=True, choices=podcastCategories)
    created_on = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']


class PodcastLoveReact(models.Model):
    post = models.ForeignKey(PodcastModel, on_delete=models.CASCADE, related_name='liked_podcast')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='podcast_liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return "{} : {}".format(self.user, self.post)


class PostsModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='resource_sharing')
    topic_name = models.CharField(max_length=100)
    post_image1 = models.ImageField(upload_to='post_images', blank=True, null=True)
    post_image2 = models.ImageField(upload_to='post_images', blank=True, null=True)
    post_image3 = models.ImageField(upload_to='post_images', blank=True, null=True)
    my_text = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]

    def str(self):
        return self.topic_name


class PostLoveReact(models.Model):
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return "{} : {}".format(self.user, self.post)


# -----------------------------syllabus--------------------------------------------#


class SyllabusModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider')
    university = models.CharField(max_length=200)
    department = models.CharField(max_length=300)
    session = models.CharField(max_length=100, blank=True, null=True)
    syllabus = models.FileField(upload_to='syllabuses/', blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.university}-{self.department}-{self.session}"


# -----------------------------end syllabus--------------------------------------------#
# -------------------------------connections--------------------------------------------#


class ConnectionModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_friends')
    connections = models.ManyToManyField(CustomUser, blank=True, related_name='friends')

    def __str__(self):
        return self.user.user_main_profile.fullName

    def add_friend(self, account):
        if account not in self.connections.all():
            self.connections.add(account)

    def remove_friend(self, account):
        if account in self.connections.all():
            self.connections.remove(account)

    def unfriend(self, removee):
        remover_friend_list = self
        remover_friend_list.remove_friend(removee)
        friendList = ConnectionModel.objects.get(user=removee)
        friendList.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.connections.all():
            return True
        return False


class ConnectionRequestModel(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.user_main_profile.fullName

    def accept(self):
        receiver_friend_list = ConnectionModel.objects.get_or_create(user=self.to_user)

        if receiver_friend_list:
            receiver_friend_list.add_friend(account=self.from_user)
            sender_friend_list = ConnectionModel.objects.get(user=self.from_user)
            if sender_friend_list:
                sender_friend_list.add_friend(account=self.to_user)
                self.is_active = True

    def decline(self):
        self.is_active = False


