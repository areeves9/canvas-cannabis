from io import BytesIO
from django.core.files.storage import default_storage


from PIL import Image, ExifTags
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def upload_location(instance, filename):
    return "%s/%s" % (instance.user, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to=upload_location,
        blank=True,
        null=True,
        height_field="height_field",
        width_field="width_field",
    )
    width_field = models.IntegerField(default=0, null=True)
    height_field = models.IntegerField(default=0, null=True)

    def __str__(self):
        return 'Profile: {}'.format(self.user)


@receiver(post_save, sender=Profile)
def update_image(sender, instance, **kwargs):
    # does the image exist?
    if instance.photo:
        image = Image.open(instance.photo)
        if hasattr(image, '_getexif'):
            try:
                # iterate through the EXIF tags
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                # get image exif metadata
                e = image._getexif()
                # check if e exists
                if e is not None:
                    # get dictionary of exif key-value pairs
                    try:
                        exif = dict(e.items())
                        if (exif[orientation]) == 3:
                            image = image.rotate(180)
                        elif (exif[orientation]) == 6:
                            image = image.rotate(270)
                        elif (exif[orientation]) == 8:
                            image = image.rotate(90)
                    except:
                        pass
            except IOError as err:
                print("I/O error: {0}".format(err))
        size = (500, 375)
        if image.width > 100:
            memfile = BytesIO()
            image.thumbnail(size, Image.ANTIALIAS)
            image.save(memfile, "JPEG")
            default_storage.save(instance.photo.name, memfile)
            memfile.close()
            image.close()


class Follow(models.Model):
    follow_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow_from'
    )
    follow_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow_to'
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '%s follows %s' % (self.follow_from, self.follow_to)


User.add_to_class(
    'following', models.ManyToManyField(
        'self',
        through=Follow,
        related_name='followers',
        symmetrical=False
    )
)
