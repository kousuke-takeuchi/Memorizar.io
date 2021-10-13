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

            <form class="card-body">
                <!-- 問題 -->
                <h4 class="mb-0">Question</h4>
                <p class="mb-4">問題の編集</p>

                <div class="row">
                    <div class="mb-3 col-12 col-md-6">
                        <label class="form-label" for="title">Title</label>
                        <input type="text" v-model="question.title" name="title" class="form-control" placeholder="タイトル" required>
                    </div>
                </div>

                <div class="mb-3 col-12 col-md-3">
                    <label class="form-label" for="sentense">Sentense</label>
                    <textarea name="sentense" cols="30" rows="10" class="form-control" placeholder="問題本文" v-model="question.sentense" required></textarea>
                </div>

                <div class="row">
                    <div class="mb-3 col-12 col-md-6">
                        <label class="form-label" for="chapter_id">Chapter</label>
                        <div class="dropdown bootstrap-select dropup" style="width: 100%;">
                            <select class="selectpicker" name="chapter_id" data-width="100%" tabindex="null" v-model="question.chapter_id">
                                <option value="">チャプターを選択してください</option>
                                <option :value="chapter.chapter_id" :key="chapter.chapter_id" v-for="chapter in chapters">{{ chapter.title }}</option>
                            </select>
                        </div>
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
                        <label class="form-label" for="collect_index">Collect Answer</label>
                        <div class="dropdown bootstrap-select dropup" style="width: 100%;">
                            <select class="selectpicker" name="collect_index" data-width="100%" tabindex="null" required>
                                <option :value="answer.index" :key="answer.index" v-for="answer in question.answers">選択肢{{ answer.index }}</option>
                            </select>
                        </div>
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
                    <button class="btn btn-primary" @click.prevent="createQuestion">Create Question</button>
                </div>
            </form>
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
    name: 'CreateQuestionPage',
    components: {
        AnswerForm,
        draggable,
    },
    data: function () {
        return {
            question: new Question(),
            chapters: JSON.parse(document.getElementById('chapters').dataset.value),
        }
    },
    async beforeMount() {
    },
    methods: {
        async createQuestion() {
            const api = new QuestionAPI();
            api.createQuestion(this.question).then(data => {
                console.log("create question");
                console.log(data);
            }).catch(error => {
                console.log(error);
            })
        }
    },
}
</script>