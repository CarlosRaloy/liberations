from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import random
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def email_user(default_code, parts, massive_changes, before_imgs, after_imgs, to_emails):
    # Asegurarse de que las listas de imágenes coincidan
    images = zip(before_imgs, after_imgs)

    context = {
        'default_code': default_code,
        'parts': parts,
        'massive_changes': massive_changes,
        'images': images  # Pasar las imágenes al contexto
    }

    template = get_template('emails/send_email.html')
    content = template.render(context)

    list_emoji = ['💰', '💲', '✪', '🔥', '🚀', '⚡', '👉', '☀', '♛', '🌟', '⌛', '👋', '🏢', '💼', '📠', '📊', '🔖', '🖋']
    list_comment = ['Un nuevo cambio', 'Cambios de productos', 'Ha llegado un nuevo cambio', 'Hey!, Ha llegado un nuevo cambio']
    ran_emoji = random.choice(list_emoji)
    ran_comment = random.choice(list_comment)

    try:
        email = EmailMultiAlternatives(
            '{} | {}'.format(ran_emoji, ran_comment),
            'Es hora de revisar el producto',
            settings.EMAIL_HOST_USER,
            to_emails
        )

        email.attach_alternative(content, 'text/html')
        EmailThread(email).start()

    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def email_edith(default_code, massive_changes, before_images, after_images, parts, to_emails):
    # Preparar los datos para el template
    context = {
        'default_code': default_code,
        'massive_changes': 'Sí' if massive_changes else 'No',
        'before_images': before_images,  # Pasar lista de imágenes 'antes'
        'after_images': after_images,  # Pasar lista de imágenes 'después'
        'parts': parts if parts else None,
    }

    # Cargar el contenido del template de email
    template = get_template('emails/edith_email.html')
    content = template.render(context)

    # Asunto personalizado
    subject = f'🚀 Solicitud modificada | {default_code}'

    # Crear y configurar el email
    email = EmailMultiAlternatives(
        subject=subject,  # Asunto personalizado
        body='Se ha modificado una solicitud',
        from_email=settings.EMAIL_HOST_USER,
        to=to_emails
    )

    # Agregar el contenido HTML
    email.attach_alternative(content, 'text/html')

    # Enviar el correo en segundo plano
    EmailThread(email).start()