import API from "./API";


export default class FlashCardAPI extends API {
    async createDeck(deck) {
        let path = `/api/flash_cards/`;
        let data = {
            'title': deck.title,
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