<template>
    <div class="pb-5 py-md-5 py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 col-md-12 col-12">
                    <div class="card">
                        <div class="d-lg-flex justify-content-between align-items-center card-header">
                            <div class="mb-3 mb-lg-0">
                                    <h3 class="mb-0 text-success" v-if="training_selection.correct">正解！ {{ training_selection.answer.title }}</h3>
                                    <h3 class="mb-0 text-danger" v-else>不正解！ {{ training_selection.answer.title }}</h3>
                                <span id="question-sentense" v-html="marked(training_selection.question.sentense)"></span>
                            </div>
                        </div>

                        

                        <div class="card-body">
                            <div class="card-deck pb-2 py-md-2 py-2">
                                <div :class="'card answer ' + answer_class(answer)" :key="answer.answer_id" v-for="answer in answers">
                                    <div class="card-body">
                                        <h5 class="card-title">{{ answer.title }} {{ answer_annotation(answer) }}</h5>
                                        <p class="card-text">{{ answer.sentense }}</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-12 pb-4 py-md-4 py-4">
                                <h3 class="mb-2">解説</h3>
                                <span id="commentary" v-html="marked(training_selection.question.commentary)"></span>
                                <div class="mb-3" v-if="training_selection.question.commentary_image_urls">
                                    <img :src="training_selection.question.commentary_image_urls[0]" style="max-height: 300px; max-width: 100%;" />
                                </div>
                            </div>

                            <div class="pb-4 py-md-4 py-4">
                                <a href="{% url 'workbooks:training_result' training_selection.training.training_id %}" v-if="training_selection.training.done" class="btn btn-primary btn-block btn-lg">結果を見る</a>
                                <a href="{% url 'workbooks:training_question' training_selection.training.training_id %}" v-else class="btn btn-primary btn-block btn-lg">次の問題</a>
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


export default {
    name: 'TrainingAnswerPage',
    components: {
    },
    data: function () {
        return {
            question: JSON.parse(document.getElementById('questions').dataset.value),
        }
    },
    methods: {
        marked: marked,
        answer_class(answer) {
            if (answer.is_true) {
                return 'answer-true'
            } else if (answer == training_selection.answer) {
                return 'answer-selection'
            }
        },
        answer_annotation(answer) {
            if (answer.is_true) {
                return '正解'
            } else if (answer == training_selection.answer) {
                return 'あなたの選択'
            }
        }
    },
}
</script>