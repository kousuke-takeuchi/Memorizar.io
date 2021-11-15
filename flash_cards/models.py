import uuid

from django.db import models
from django.contrib.auth.models import User

from lib.models import BaseModel
from . import managers


class FlashCardDeck(BaseModel, models.Model):
    deck_id = models.UUIDField('デッキID', default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=250, db_index=True)

    objects = managers.FlashCardDeckManager()

    class Meta:
        verbose_name = 'flash_card_decks'
        verbose_name_plural = 'FlashCardDeck'

    def __str__(self):
        return str(self.title)


class FlashCard(BaseModel, models.Model):
    flash_card_id = models.UUIDField('カードID', default=uuid.uuid4, unique=True, db_index=True)
    deck = models.ForeignKey('flash_cards.FlashCardDeck', db_index=True, on_delete=models.CASCADE)
    front_sentense = models.TextField('表')
    back_sentense = models.TextField('裏')

    objects = managers.FlashCardManager()

    class Meta:
        verbose_name = 'flash_cards'
        verbose_name_plural = 'FlashCard'

    def __str__(self):
        return str(self.front_sentense)