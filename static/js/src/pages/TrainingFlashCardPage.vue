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
            deckId: deckId,
            deck: null,
            api: api,
        }
    },
    async beforeMount() {
        this.api.getFlashCard(this.deckId).then(deck => {
            this.deck = deck;
        });
    },
    methods: {
    },
}
</script>