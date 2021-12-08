from rest_framework import serializers

from . import models


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlashCard
        read_only_fields = ('flash_card_id',)
        write_only_fields = ()
        fields = read_only_fields + write_only_fields + ('front_sentense', 'back_sentense',)
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])


class FlashCardDeckSerializer(serializers.ModelSerializer):
    flash_cards = FlashCardSerializer(many=True)

    class Meta:
        model = models.FlashCardDeck
        read_only_fields = ('deck_id',)
        write_only_fields = ()
        fields = read_only_fields + write_only_fields + ('title', 'flash_cards',)
        extra_kwargs = dict([(field, {'write_only': True, 'required': True}) for field in write_only_fields])
    
  
    def create(self, validated_data):
        deck = models.FlashCardDeck.objects.create(
            title=validated_data['title'],
            user=self.context['request'].user,
        )
        for flash_card_data in validated_data['flash_cards']:
            models.FlashCard.objects.create(
                deck=deck,
                front_sentense=flash_card_data['front_sentense'],
                back_sentense=flash_card_data['back_sentense'],
            )
        return deck