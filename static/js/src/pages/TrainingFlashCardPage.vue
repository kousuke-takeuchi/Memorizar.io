<template>
    <div class="pb-5 py-md-5 py-5" v-if="deck">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 col-md-12 col-12">
                    <div class="card">
                        <div class="justify-content-between align-items-center card-header">
                            <div class="mb-3 mb-lg-0">
                                <h3 class="mb-0">{{ deck.title }}</h3>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="card col-6 flash-card flash-card-back" :class="empty('back')" @click="back">
                                    <p>{{ previousCard ? previousCard.back_sentense : '' }}</p>
                                    <span class="dot"></span>
                                </div>
                                <div class="card col-6 flash-card flash-card-front" :class="empty('front')" @click="next">
                                    <p>{{ currentCard ? currentCard.front_sentense : '' }}</p>
                                    <span class="dot"></span>
                                </div>
                            </div>
                            <a class="btn btn-primary mt-6" href="/flash_cards/">Finish</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="js">
import marked from 'marked';

import FlashCardAPI from '../apis/FlashCardAPI';


export default {
    name: 'TrainingFlashCardPage',
    data() {
        let regex = /.*\/flash_cards\/([0-9a-z\-]+)\/training+/i
        let url = window.location.href;
        let deckId = url.match(regex)[1];
        let token = document.getElementById('token').dataset.value
        let api = new FlashCardAPI(token);
        return {
            previousCard: null,
            currentCard: null,
            currentIndex: 0,
            deckId: deckId,
            deck: null,
            api: api,
        }
    },
    async beforeMount() {
        this.api.getFlashCard(this.deckId).then(deck => {
            this.deck = deck;
            if (this.deck.flash_cards.length > 0) {
                this.currentCard = this.deck.flash_cards[0];
                console.log(this.currentCard)
            }
        });
    },
    methods: {
        back() {
            if (this.currentIndex > 0) {
                this.currentIndex--;
                this.currentCard = this.deck.flash_cards[this.currentIndex];
                if (this.currentIndex != 0) {
                    this.previousCard = this.deck.flash_cards[this.currentIndex-1];
                } else {
                    this.previousCard = null;
                }
            }
        },
        next() {
            if (this.currentIndex < this.deck.flash_cards.length) {
                this.currentIndex++;
                this.currentCard = this.deck.flash_cards[this.currentIndex];
                this.previousCard = this.deck.flash_cards[this.currentIndex-1];
            }
        },
        empty(pos) {
            if (this.flash_cards === null) {
                return 'empty';
            }
            if (pos == 'front') {
                return this.currentIndex < this.deck.flash_cards.length ? '' : 'empty';
            } else if (pos == 'back') {
                return this.currentIndex > 0 ? '' : 'empty';
            }
        }
    },
}
</script>


<style scoped>
    .flash-card {
        min-height: 150px;
        position: relative;
        box-shadow: 0 1px 3px rgb(3 0 71 / 30%);
    }

    .flash-card .dot {
        height: 25px;
        width: 25px;
        background-color: #efefef;
        border: solid 1px #efefef;
        border-radius: 50%;
        display: inline-block;
        position: absolute;
        top: 40%;
    }

    .flash-card.flash-card-front .dot {
        left: 20px;
    }

    .flash-card.flash-card-back .dot {
        right: 20px;
    }

    .flash-card.empty {
        box-shadow: none;
    }

    .flash-card.empty .dot {
        display: none;
    }
</style>