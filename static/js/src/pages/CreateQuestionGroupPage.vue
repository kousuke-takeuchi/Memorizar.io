<template>
<!-- 問題作成フォーム -->
<div class="container pt-5 pb-5">
    <div class="lg-12 md-12 col-12"> 
        <div class="card">
            <div class="d-lg-flex justify-content-between align-items-center card-header">
                <div class="mb-3 mb-lg-0">
                    <h3 class="mb-0">Create a new Question</h3>
                    <span>問題の新規作成</span>
                </div>
            </div>

            <form id="form" class="card-body">
                <h4 class="mb-0">QuestionGroup</h4>
                <p class="mb-4">問題グループの編集</p>

                <div class="row">
                    <div class="mb-3 col-12 col-md-6">
                        <label class="form-label" for="title">Title</label>
                        <input type="text" name="title" class="form-control" :class="{'is-invalid': errors.title}" placeholder="タイトル" required>
                        <div id="validationTitleFeedback" class="invalid-feedback" v-if="errors.title">{{ errors.title }}</div>
                    </div>
                </div>

                <div class="mb-12 col-12 col-md-12">
                    <label class="form-label" for="sentense">Sentense</label>
                    <textarea name="sentense" cols="30" rows="10" class="form-control" :class="{'is-invalid': errors.description}" placeholder="問題本文" required></textarea>
                    <div id="validationDescriptionFeedback" class="invalid-feedback" v-if="errors.description">{{ errors.description }}</div>
                </div>

                <div class="row">
                    <div class="mb-3 col-12 col-md-6">
                        <label class="form-label" for="chapter_id">Chapter</label>
                        <select class="form-select" name="chapter_id" data-width="100%" tabindex="null">
                            <option value="" selected disabled>チャプターを選択してください</option>
                            <option :value="chapter.chapter_id" :key="chapter.chapter_id" v-for="chapter in chapters">{{ chapter.title }}</option>
                        </select>
                    </div>
    
                    <div class="custom-file mb-3 col-12 col-md-6">
                        <label class="form-label" for="image">Figure (Option)</label>
                        <input type="file" class="form-control custom-file-input" name="image">
                    </div>
                </div>

                <hr class="my-5">

                <!-- 問題 -->
                <div :key="index" v-for="question, index in questionGroup.questions">
                    <h4 class="mb-0">Question</h4>
                    <p class="mb-4">問題の編集</p>

                    <div class="row">
                        <div class="mb-3 col-12 col-md-6">
                            <label class="form-label" for="title">Title</label>
                            <input type="text" name="title" class="form-control" :class="{'is-invalid': errors.title}" placeholder="タイトル" required>
                            <div id="validationTitleFeedback" class="invalid-feedback" v-if="errors.title">{{ errors.title }}</div>
                        </div>
                    </div>

                    <div class="mb-12 col-12 col-md-12">
                        <label class="form-label" for="sentense">Sentense</label>
                        <textarea name="sentense" cols="30" rows="10" class="form-control" :class="{'is-invalid': errors.description}" placeholder="問題本文" required></textarea>
                        <div id="validationDescriptionFeedback" class="invalid-feedback" v-if="errors.description">{{ errors.description }}</div>
                    </div>

                    <div class="row">
                        <div class="custom-file mb-3 col-12 col-md-6">
                            <label class="form-label" for="image">Figure (Option)</label>
                            <input type="file" class="form-control custom-file-input" name="image">
                        </div>
                    </div>

                    <hr class="my-5">

                    <!-- 回答選択肢 -->
                    <h4 class="mb-0">Selections</h4>
                    <p class="mb-4">回答選択肢 (4つ)</p>

                    <draggable class="row" @change.prevent="onChangedAnswers">
                        <AnswerForm :answer="answer" :key="answer.index" v-for="answer in question.answers" />
                    </draggable>

                    <div class="row">
                        <div class="mb-3 col-12 col-md-6">
                            <label class="form-label" for="correct_index">Correct Answer</label>
                            <select class="form-select" name="correct_index" data-width="100%" tabindex="null" required>
                                <option :value="answer.index" :key="answer.index" v-for="answer in question.answers">選択肢{{ answer.index }}</option>
                            </select>
                        </div>
                    </div>

                    <div class="col-12">
                        <button class="btn btn-secondary">Add Selection</button>
                    </div>

                    <hr class="my-5">

                    <!-- 解説文 -->
                    <h4 class="mb-0">Answer Commentary</h4>
                    <p class="mb-4">正解の選択肢についての解説</p>
                    
                    <div class="mb-3 col-12 col-md-12">
                        <label class="form-label" for="commentary">Commentary</label>
                        <textarea name="commentary" cols="30" rows="10" class="form-control" :class="{'is-invalid': errors.commentary}" placeholder="問題本文" required></textarea>
                        <div id="validationCommentaryFeedback" class="invalid-feedback" v-if="errors.commentary">{{ errors.commentary }}</div>
                    </div>

                    <div class="custom-file mb-3 col-12 col-md-6">
                        <label class="form-label" for="chapter_id">Figure (Option)</label>
                        <input type="file" class="form-control custom-file-input" name="commentary_image">
                    </div>

                    <hr class="my-5">
                </div>

                <!-- 問題追加ボタン -->
                <div class="col-12">
                    <button class="btn btn-secondary" @click.prevent="addQuestion">Add Another Question</button>
                </div>

                <hr class="my-5">

                <!-- 送信ボタン -->
                <div class="col-12">
                    <button class="btn btn-primary" @click.prevent="createQuestionGroup">Create Question</button>
                </div>
            </form>
        </div>
    </div>
</div>
</template>


<script lang="js">
import draggable from 'vuedraggable';

import QuestionGroup from '../models/QuestionGroup';
import Question from '../models/Question';
import AnswerForm from '../components/AnswerForm';
import QuestionAPI from '../apis/QuestionAPI';


export default {
    name: 'CreateQuestionGroupPage',
    components: {
        AnswerForm,
        draggable,
    },
    data: function () {
        let regex = /.*\/workbooks\/([0-9a-z\-]+)\/questions\/new_group\/+/i
        let url = window.location.href;
        let workbookId = url.match(regex)[1];
        let token = document.getElementById('token').dataset.value
        let api = new QuestionAPI(token);
        return {
            workbookId: workbookId,
            api: api,
            questionGroup: new QuestionGroup(),
            chapters: JSON.parse(document.getElementById('chapters').dataset.value),
            errors: {},
        }
    },
    beforeMount() {
        // question_group_idが指定されている場合は複製する
        let uri = window.location.search.substring(1);
        let params = new URLSearchParams(uri);
        let questionGroupId = params.get("question_group_id");
        if (questionGroupId) {
            this.api.getQuestionGroup(this.workbookId, questionGroupId).then(questionGroup => {
                this.questionGroup = questionGroup;
            });
        }
    },
    methods: {
        addQuestion() {
            this.questionGroup.addNewQuestion();
        },
        async createQuestionGroup() {
            this.api.createQuestion(workbookId, this.question).then(data => {
                window.location.href = window.location.href.replace('/questions/new', '');
            }).catch(error => {
                this.errors = {};
                for (let error of error.data.errors) {
                    this.errors[error.field] = error.message;
                }
            })
        }
    },
}
</script>