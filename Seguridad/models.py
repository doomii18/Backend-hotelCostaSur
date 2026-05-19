import hashlib
from django.db import models


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50, unique=True)
    correo = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, default='user')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.usuario} ({self.rol})"

    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256 to match previous session encoding."""
        if not password:
            return ""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def set_password(self, raw_password):
        self.contrasena = self.hash_password(raw_password)

    def check_password(self, raw_password):
        return self.contrasena == self.hash_password(raw_password)


class Cliente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('cedula', 'Cédula'),
        ('pasaporte', 'Pasaporte'),
    ]
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]

    id = models.IntegerField(primary_key=True)  # Primary key is 'id' matching the script
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='clientes'
    )
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    pais_pasaporte = models.CharField(max_length=50, null=True, blank=True)
    pasaporte = models.CharField(max_length=50, null=True, blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)
    procedencia = models.CharField(max_length=100)
    Estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
