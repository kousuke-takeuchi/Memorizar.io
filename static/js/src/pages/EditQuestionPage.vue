<template>
    <div>

        <!-- 問題編集フォーム -->
        <div class="container pt-5 pb-5">
            <div class="lg-12 md-12 col-12"> 
                <div class="card">
                    <div class="d-lg-flex justify-content-between align-items-center card-header">
                        <div class="mb-3 mb-lg-0">
                            <h3 class="mb-0">Update Question</h3>
                            <span>問題の編集</span>
                        </div>
                        <a class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteQuestionModal" href="#">Delete</a>
                    </div>

                    <form class="card-body">
                        <!-- 問題 -->
                        <h4 class="mb-0">Question</h4>

                        <div class="row">
                            <div class="mb-3 col-12 col-md-6">
                                <label class="form-label" for="title">Title</label>
                                <input type="text" v-model="question.title" name="title" class="form-control" placeholder="タイトル" required>
                            </div>
                        </div>

                        <div class="mb-12 col-12 col-md-12">
                            <label class="form-label" for="sentense">Sentense</label>
                            <textarea name="sentense" cols="30" rows="10" class="form-control" placeholder="問題本文" v-model="question.sentense" required></textarea>
                        </div>

                        <div class="row">
                            <div class="mb-3 col-12 col-md-6">
                                <label class="form-label" for="chapter_id">Chapter</label>
                                <select class="form-select" name="chapter_id" data-width="100%" tabindex="null" v-model="question.chapter_id">
                                    <option :value="chapter.chapter_id" :key="chapter.chapter_id" v-for="chapter in chapters">{{ chapter.title }}</option>
                                </select>
                            </div>
            
                            <div class="custom-file mb-3 col-12 col-md-6">
                                <label class="form-label" for="chapter_id">Figure (Option)</label>
                                <input type="file" class="form-control custom-file-input" name="image">
                            </div>
                        </div>

                        <hr class="my-5">

                        <!-- 回答選択肢 -->
                        <h4 class="mb-0">Selections</h4>
                        <p class="mb-4">回答選択肢 (4つ)</p>

                        <draggable class="row" v-model="question.answers">
                            <AnswerForm :answer="answer" :key="answer.index" v-for="answer in question.answers" />
                        </draggable>

                        <div class="row">
                            <div class="mb-3 col-12 col-md-6">
                                <label class="form-label" for="correct_index">Correct Answer</label>
                                <select class="form-select" name="correct_index" data-width="100%" tabindex="null" v-model="question.correct_index" required>
                                    <option :value="answer.index" :key="answer.index" v-for="answer in question.answers">選択肢{{ answer.index }}</option>
                                </select>
                            </div>
                        </div>

                        <div class="col-12">
                            <button class="btn btn-secondary" @click="question.addNewAnswer()">Add Selection</button>
                        </div>

                        <hr class="my-5">

                        <!-- 解説文 -->
                        <h4 class="mb-0">Answer Commentary</h4>
                        <p class="mb-4">正解の選択肢についての解説</p>
                        
                        <div class="mb-3 col-12 col-md-12">
                            <label class="form-label" for="commentary">Commentary</label>
                            <textarea name="commentary" cols="30" rows="10" class="form-control" placeholder="問題本文" v-model="question.commentary" required></textarea>
                        </div>

                        <div class="custom-file mb-3 col-12 col-md-6">
                            <input type="file" class="form-control custom-file-input" name="commentary_image">
                        </div>

                        <hr class="my-5">

                        <!-- 送信ボタン -->
                        <div class="col-12">
                            <button class="btn btn-primary" @click.prevent="editQuestion">Create Question</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- 削除確認モーダル -->
        <div class="modal fade" id="deleteQuestionModal" tabindex="-1" aria-labelledby="delete-modal" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="delete-modal">チャプターを削除</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form method="POST" action="{% url 'workbooks:question_delete' workbook_id=workbook.workbook_id question_id=question.question_id %}">
                        <div class="modal-body">
                            <p>一度削除すると元に戻すことはできません。(実施履歴は残ります)</p>
                            <p>削除してもよろしいですか？</p>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
                            <button type="submit" class="btn btn-danger" id="start-delete-btn" @click.prevent="onClickDelete">削除</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

</template>


<script lang="js">
import draggable from 'vuedraggable';

import Question from '../models/Question';
import AnswerForm from '../components/AnswerForm';
import QuestionAPI from '../apis/QuestionAPI';


export default {
    name: 'EditQuestionPage',
    components: {
        AnswerForm,
        draggable,
    },
    data: function () {
        const regex = /.*\/workbooks\/([0-9a-z\-]+)\/questions\/([0-9a-z\-]+)\/edit\/+/i
        const url = window.location.href;
        const workbookId = url.match(regex)[1];
        const questionId = url.match(regex)[2];
        const token = document.getElementById('token').dataset.value
        const api = new QuestionAPI(token);

        return {
            question: new Question(),
            chapters: JSON.parse(document.getElementById('chapters').dataset.value),
            workbookId: workbookId,
            questionId: questionId,
            api: api,
        }
    },
    async beforeMount() {
        this.api.getQuestion(this.workbookId, this.questionId).then(question => {
            this.question = question;
        }).catch(error => {
            console.log(error);
        });
    },
    methods: {
        async editQuestion() {
            this.api.editQuestion(this.workbookId, this.question).then(data => {
                window.location.href = window.location.href.replace('/questions/new', '');
            }).catch(error => {
                console.log(error);
            })
        },
        async onClickDelete() {
            this.api.deleteQuestion(this.workbookId, this.question).then(data => {
                window.location.href = `/workbooks/${this.workbookId}/`;
            }).catch(error => {
                console.log(error);
            })
        }
    },
}
</script>