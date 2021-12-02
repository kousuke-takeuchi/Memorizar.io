<template>
    <div class="row mb-2">
        <div class="col-12 col-md-5">
            <label class="form-label" for="title">({{ index }}) 問題タイトル</label>
            <input type="text" class="form-control" name="title" />
        </div>

        <div class="col-12 col-md-2">
            <label class="form-label" for="answer_num">回答選択肢数</label>
            <input type="number" class="form-control" name="answer_num" :value="question.answers.length" />
        </div>

        <div class="col-12 col-md-3">
            <label class="form-label" for="correct_index">正解番号</label>
            <select class="form-select" name="correct_index" data-width="100%" tabindex="null" v-model="question.correct_index" required>
                <option :value="answer.index" :key="answer.index" v-for="answer in question.answers">選択肢{{ answer.index }}</option>
            </select>
        </div>

        <div class="col-12 col-md-2">
            <label class="form-label" for="correct_index">対応する解説番号</label>
            <select class="form-select" name="correct_index" data-width="100%" tabindex="null" required>
                <option :value="answer.index" :key="answer.index" v-for="answer in question.answers">{{ answer.index }}</option>
            </select>
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