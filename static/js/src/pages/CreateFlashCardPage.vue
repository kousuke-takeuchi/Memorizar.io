<template>
    <!-- フラッシュカード作成フォーム -->
    <div class="container pt-5 pb-5">
        <div class="lg-12 md-12 col-12"> 
            <div class="card">
                <div class="d-lg-flex justify-content-between align-items-center card-header">
                    <div class="mb-3 mb-lg-0">
                        <h3 class="mb-0">Create a new FlashCard</h3>
                        <span>フラッシュカードの新規作成</span>
                    </div>
                </div>

                <form id="form" class="card-body">
                    <!-- 問題 -->
                    <h4 class="mb-0">Deck</h4>
                    <p class="mb-4">デッキの編集</p>

                    <div class="row">
                        <div class="mb-3 col-12 col-md-6">
                            <label class="form-label" for="title">Title</label>
                            <input type="text" v-model="deck.title" name="title" class="form-control" :class="{'is-invalid': errors.title}" placeholder="タイトル" required>
                            <div id="validationTitleFeedback" class="invalid-feedback" v-if="errors.title">{{ errors.title }}</div>
                        </div>
                    </div>

                    <hr class="my-5">

                    <!-- カード一覧 -->
                    <h4 class="mb-0">FlashCard</h4>
                    <p class="mb-4">フラッシュカード</p>

                    <div class="row">
                        <FlashCardForm :flash_card="flash_card" :key="flash_card.index" v-for="flash_card in deck.flash_cards" @clickDelete="deleteFlashCard" />
                    </div>

                    <div class="col-12">
                        <button class="btn btn-secondary" @click.prevent="deck.addNewFlashCard()">Add Card</button>
                    </div>

                    <hr class="my-5">

                    <!-- 送信ボタン -->
                    <div class="col-12">
                        <button class="btn btn-primary" @click.prevent="createDeck">Create Deck</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>


<script lang="js">
import { FlashCardDeck } from '../models/FlashCard';
import FlashCardForm from '../components/FlashCardForm';
import FlashCardAPI from '../apis/FlashCardAPI';

export default {
    name: 'CreateFlashCardPage',
    components: {
        FlashCardForm,
    },
    data: function () {
        let token = document.getElementById('token').dataset.value
        let api = new FlashCardAPI(token);
        return {
            api: api,
            deck: new FlashCardDeck(),
            errors: {},
        }
    },
    methods: {
        deleteFlashCard(index) {
            this.deck.deleteFlashCard(index);
        },
        async createDeck() {
            this.api.createDeck(this.deck).then(data => {
                window.location.href = window.location.href.replace('/new', '');
            }).catch(error => {
                console.log(error)
                this.errors = {};
                for (let e of error.data.errors) {
                    this.errors[e.field] = e.message;
                }
            })
        }
    },
}
</script>