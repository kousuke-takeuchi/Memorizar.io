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
                                    <div class="card answer col-md-5 m-lg-1 col-12 m-1" :class="{ 'answer-selection':  answer.selected}" @click="selectAnswer(answer.answer_id)" :data-answer-id="answer.answer_id" :key="answer.answer_id" v-for="answer in question.answers">
                                        <div class="card-body">
                                            <h5 class="card-title">({{ answer.title }})</h5>
                                            <p class="card-text">{{ answer.sentense }}</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="pb-4 py-md-4 py-4">
                                    <button type="submit" class="btn btn-primary btn-block btn-lg" @click.prevent="sendSelection" :disabled="!didSelected">回答を見る</button>
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

import Question from '../models/Question';
import TrainingAPI from '../apis/TrainingAPI';


export default {
    name: 'TrainingQuestionPage',
    components: {
    },
    data: function () {
        const question = Question.load_data(
            JSON.parse(document.getElementById('questions').dataset.value),
            JSON.parse(document.getElementById('answers').dataset.value)
        );
        return {
            selected_answer: null,
            question: question,
            start_at: JSON.parse(document.getElementById('start_at').dataset.value),
            didSelected: false,
        }
    },
    async beforeMount() {
    },
    methods: {
        selectAnswer(answerId) {
            this.question.selectAnswer(answerId);
            this.didSelected = true;
        },
        async sendSelection() {
            const regex = /.*\/workbooks\/([0-9a-z\-]+)\/trainings\/([0-9a-z\-]+)\/question+/i
            const url = window.location.href;
            const workbookId = url.match(regex)[1];
            const trainingId = url.match(regex)[2];
            const token = document.getElementById('token').dataset.value;
            const api = new TrainingAPI(token);
            api.createSelection(workbookId, trainingId, this.question, this.start_at).then(selection => {
                window.location.href = `/workbooks/${workbookId}/trainings/${trainingId}/selections/${selection.training_selection_id}/`;
            }).catch(error => {
                console.log(error);
            })
        },
        marked: marked,
    },
}
</script>