from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from lib import mixins
from lib.responses import SuccessResponse, ErrorResponse
from . import models, serializers


class FlashCardDeckListView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self):
        decks = models.FlashCardDeck.objects.filter(user=self.request.user)
        return decks
        
    def get(self, request):
        querysets = self.get_querysets()
        serializer = serializers.FlashCardDeckSerializer(querysets, many=True, context={'request': request})
        return SuccessResponse({'decks': serializer.data})
    
    def post(self, request):
        serializer = serializers.FlashCardDeckSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            return ErrorResponse(serializer.errors)
        serializer.save()
        return SuccessResponse({})


class FlashCardDeckDetailView(mixins.MemorizarBaseMixin, APIView):
    def get_querysets(self, deck_id):
        deck = get_object_or_404(models.FlashCardDeck, deck_id=deck_id)
        return deck
        
    def get(self, request, deck_id):
        querysets = self.get_querysets(deck_id)
        serializer = serializers.FlashCardDeckSerializer(querysets, context={'request': request})
        return SuccessResponse({'deck': serializer.data})