from django.db import models

class Achievements(models.Model):
    team = models.ForeignKey('sports_base.Team', related_name='achievements', on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.description[:50]}..."

class HomePic(models.Model):
    image = models.ImageField(upload_to='carousel/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carousel Image {self.id}"

class HODMessage(models.Model):
    name = models.CharField(max_length=100, default="Professor Dr. Tahir")
    message = models.TextField(default="Keeping in view the challenges posed to man by emerging trends of the present millennium, we have introduced a system of education that is based on the lines and parameters of modern approaches in the field of science and education.")
    image = models.ImageField(upload_to='hod_photos/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name