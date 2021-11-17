import time
import math

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse

from lib import mixins
from . import models


class FlashCardDeckListView(mixins.BaseMixin, View):
    template_name = 'flash_cards/list.html'

    def get_querysets(self):
        decks = models.FlashCardDeck.objects.filter(user=self.request.user)
        p = Paginator(decks, 10)
        page = self.request.GET.get('page', 1)
        return p.page(page)
    
    def get(self, request):
        # フラッシュカード一覧
        decks = self.get_querysets()
        context = dict(decks=decks)
        return render(request, self.template_name, context)


class FlashCardDeckCreateView(mixins.BaseMixin, View):
    template_name = 'flash_cards/new.html'
    
    def get(self, request):
        context = dict()
        return render(request, self.template_name, context)


class FlashCardDeckDetailView(mixins.BaseMixin, View):
    template_name = 'flash_cards/detail.html'

    def get_querysets(self, deck_id):
        deck = get_object_or_404(models.FlashCardDeck, deck_id=deck_id)
        return deck
    
    def get(self, request, deck_id):
        deck = self.get_querysets(deck_id)
        context = dict(deck=deck)
        return render(request, self.template_name, context)


class FlashCardTrainingView(mixins.BaseMixin, View):
    template_name = 'flash_cards/training.html'
    
    def get(self, request, deck_id):
        context = dict()
        return render(request, self.template_name, context)