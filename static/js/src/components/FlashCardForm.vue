<template>
    <div class="card-group mb-6">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Front</h5>
                <input type="text" class="card-text form-control" placeholder="表" v-model="flash_card.front_sentense" />
            </div>
        </div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Back</h5>
                <input type="text" class="card-text form-control" placeholder="裏" v-model="flash_card.back_sentense" />
            </div>
        </div>
    </div>
</template>


<script lang="js">

import { FlashCard } from '../models/FlashCard';

export default {
    name: 'FlashCardForm',
    props: {
        flash_card: FlashCard,
    },
    methods: {
        onClickDelete(index) {
            this.$emit('clickDelete', index);
        }
    },
}
</script>