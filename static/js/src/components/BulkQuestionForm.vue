<template>
    <div class="row">
        <div class="mb-3 col-12 col-md-9">
            <label class="form-label" for="title">({{ index }}) 問題タイトル</label>
            <input type="text" class="form-control" name="title" />
        </div>

        <div class="mb-3 col-12 col-md-3">
            <label class="form-label" for="title">回答選択肢数</label>
            <input type="number" class="form-control" name="title" :value="question.answers.length" />
        </div>
    </div>
</template>


<script lang="js">

import Question from '../models/Question';

export default {
    name: 'AnswerForm',
    props: {
        question: Question,
        index: Number,
    },
}
</script>