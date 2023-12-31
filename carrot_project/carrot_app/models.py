from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Image(models.Model):
    image = models.ImageField(upload_to="post_images/")


class Post(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)  # 다중 이미지 관계 설정
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)

    product_reserved = models.CharField(max_length=1, default="N")  # 예약 여부
    product_sold = models.CharField(max_length=1, default="N")  # 판매 여부

    view_num = models.PositiveIntegerField(default=0)  # 조회 수
    chat_num = models.PositiveIntegerField(default=0)  # 채팅 수

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    birthdate = models.DateField(null=True)
    gender = models.CharField(
        max_length=1, choices=[("남", "남자"), ("여", "여자"), ("O", "설정 않음")], null=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="profile_pictures/default_profile_picture.png"  # 기본 프로필 사진 경로
    )
    region = models.CharField(max_length=100, null=True)
    region_certification = models.CharField(max_length=1, default="N")


    def __str__(self):
        return f"{self.user.username} Profile"

class MannerTemperature(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="manner_temperature"
    )
    total_votes = models.PositiveIntegerField(default=1)  # 전체 투표 수
    total_score = models.PositiveIntegerField(default=30)  # 전체 점수 합
    
    def average_temperature(self):
        if self.total_votes > 0:
            return round(self.total_score / self.total_votes, 1)
        else:
            return 0.0

    def update_temperature(self, score):
        self.total_votes += 1
        self.total_score += score
        self.save()


class ChatRoom(models.Model):
    room_number = models.AutoField(primary_key=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    latest_message_time = models.DateTimeField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_rooms', null=True, blank=True)


    def __str__(self):
        return f'ChatRoom: {self.starter.username} and {self.receiver.username}'

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: {self.author.username} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 새 메시지가 저장될 때마다 chatroom의 latest_message_time을 업데이트
        self.chatroom.latest_message_time = self.timestamp
        self.chatroom.save()

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
