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


def email_user(default_code, change_code, parts, massive_changes):
    context = {
        'default_code': default_code,
        'change_code': change_code,
        'parts': parts,
        'massive_changes': massive_changes
    }
    template = get_template('emails/send_email.html')
    content = template.render(context)

    list_emoji = ['💰', '💲', '✪', '🔥', '🚀', '⚡', '👉', '☀', '♛', '🌟', '⌛', '👋', '🏢', '💼', '📠', '📊', '🔖', '🖋']
    list_comment = ['Un nuevo cambio', 'Cambios de productos', 'Ha llegado un nuevo cambio',
                    'Hey!, Ha llegado un nuevo cambio']
    ran_emoji = random.choice(list_emoji)
    ran_comment = random.choice(list_comment)

    email = EmailMultiAlternatives(
        '{} | {}'.format(ran_emoji, ran_comment),
        'Es hora de revisar el producto',
        settings.EMAIL_HOST_USER,
        ['cgarcia@raloy.com.mx', ]
    )

    email.attach_alternative(content, 'text/html')
    EmailThread(email).start()