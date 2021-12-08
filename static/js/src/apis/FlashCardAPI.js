import API from "./API";
import { FlashCardDeck, FlashCard } from '../models/FlashCard';


export default class FlashCardAPI extends API {
    async getFlashCard(deckId) {
        let path = `/api/flash_cards/${deckId}/`;
        let resp = await this.get(path, {});
        let deckData = resp.data.deck;
        console.log(deckData);
        let deck = new FlashCardDeck();
        deck.title = deckData.title;
        deck.deck_id = deckData.deck_id;
        let index = 0;
        for (let cardData of deckData.flash_cards) {
            let card = new FlashCard();
            card.index = index;
            card.flash_card_id = cardData.flash_card_id;
            card.front_sentense = cardData.front_sentense;
            card.back_sentense = cardData.back_sentense;
            deck.flash_cards.push(card);
            index++;
        }
        deck.size = index;
        return deck;
    }

    async createDeck(deck) {
        let path = `/api/flash_cards/`;
        let data = {
            'title': deck.title,
            'flash_cards': [],
        }
        for (let flash_card of deck.flash_cards) {
            let form = {
                'front_sentense': flash_card.front_sentense,
                'back_sentense': flash_card.back_sentense,
            };
            data['flash_cards'].push(form);
        }
        return this.post(path, data);
    }
}