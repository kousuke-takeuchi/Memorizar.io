<template>
    <div class="pb-5 py-md-5 py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 col-md-12 col-12">
                    <div class="card">
                        <div class="justify-content-between align-items-center card-header">
                            <div class="mb-3 mb-lg-0">
                                <h3 class="mb-0">{{ question.title }}</h3>
                                <span id="question-sentense" v-html="marked(question.sentense)"></span>
                            </div>
                            <div class="mb-3" v-if="question.image_urls">
                                <img :src="question.image_urls[0]" style="max-height: 300px; max-width: 100%;" />
                            </div>
                        </div>

                        <form method="POST">
                            <input type="hidden" name="selected_id" value="" />
                            <input type="hidden" name="question_id" :value="question.question_id" />
                            <input type="hidden" name="start_at" :value="start_at" />

                            <div class="card-body">
                                <div class="row card-deck">
                                    <div class="card answer pt-2 pb-2 py-md-2 py-2 col-6" :data-answer-id="answer.answer_id" :key="answer.answer_id" v-for="answer in answers">
                                        <div class="card-body">
                                            <h5 class="card-title">({{ answer.title }})</h5>
                                            <p class="card-text">{{ answer.sentense }}</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="pb-4 py-md-4 py-4">
                                    <button type="submit" class="btn btn-primary btn-block btn-lg" @click.prevent="sendSelection" disabled>回答を見る</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="js">
import marked from 'marked';

import QuestionAPI from '../apis/QuestionAPI';


// $('.answer').on('click', function (e) {
//     $('.answer').removeClass('answer-selection');
//     $(e.currentTarget).addClass('answer-selection');
//     $('input[name="selected_id"]').val($(e.currentTarget).data('answer-id'));
//     $('button[type="submit"]').removeAttr('disabled');
// });

export default {
    name: 'TrainingQuestionPage',
    components: {
    },
    data: function () {
        return {
            selected_answer: null,
            question: JSON.parse(document.getElementById('questions').dataset.value),
            answers: JSON.parse(document.getElementById('answers').dataset.value),
            start_at: JSON.parse(document.getElementById('start_at').dataset.value),
        }
    },
    async beforeMount() {
    },
    methods: {
        async sendSelection() {
            const regex = /http:\/\/.*\/workbooks\/([0-9a-z\-]+)\/questions\/new\/+/i
            const url = window.location.href;
            const workbookId = url.match(regex)[1];
            const token = document.getElementById('token').dataset.value
            const api = new QuestionAPI(token);
            api.createQuestion(workbookId, this.question).then(data => {
                window.location.href = window.location.href.replace('/questions/new', '');
            }).catch(error => {
                console.log(error);
            })
        },
        marked: marked,
    },
}
</script>