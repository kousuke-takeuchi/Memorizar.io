export class FlashCardDeck {
    constructor() {
        this.deck_id = null;
        this.title = '';
        this.flash_cards = [];
        this.size = 0;
    }

    addNewFlashCard() {
        var index = this.size;
        this.flash_cards.push(new FlashCard(index+1));
        this.size++;
    }

    deleteFlashCard(index) {
        if (this.size > 0) {
            this.flash_cards.splice(index-1, 1);
            this.size--;

            for (var i = 0; i < this.size; i++) {
                var index = i + 1;
                this.flash_cards[i].index = index
            }
        }
    }
}

export class FlashCard {
    constructor(index) {
        this.index = index;
        this.front_sentense = '';
        this.back_sentense = '';
    }
}