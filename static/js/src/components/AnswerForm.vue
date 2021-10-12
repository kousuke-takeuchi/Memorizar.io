<template>
    <div class="mb-3 col-12 col-md-6">
        <div class="mb-3 col-12 col-md-12">
            <label class="form-label" for="sentense">({{ answer.index }})</label>
            <textarea name="sentense" cols="30" rows="3" class="form-control" :placeholder="'回答選択肢'" v-model="answer.sentense" required></textarea>
        </div>
    </div>
</template>


<script lang="js">

import Answer from '../models/Answer';

export default {
    name: 'AnswerForm',
    props: {
        answer: Answer,
    },
    components: {
    },
    async beforeMount() {
    },
    methods: {
    },
}
</script>