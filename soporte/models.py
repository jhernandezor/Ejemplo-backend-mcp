from django.db import models

class Ticket(models.Model):
    asunto = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'

    def __str__(self):
        return f"#{self.id} - {self.asunto}"