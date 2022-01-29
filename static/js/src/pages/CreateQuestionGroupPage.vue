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
                        <input type="text" name="title" class="form-control" :class="{'is-invalid': errors.title}" v-model="questionGroup.title" placeholder="タイトル" required>
                        <div id="validationTitleFeedback" class="invalid-feedback" v-if="errors.title">{{ errors.title }}</div>
                    </div>
                </div>

                <div class="mb-12 col-12 col-md-12">
                    <label class="form-label" for="sentense">Sentense</label>
                    <quill-editor
                            v-model='questionGroup.sentense'
                            ref='textEditor'
                            :options='editorOption'
                            class="from-control"
                            :class="{'is-invalid': errors.sentense}"
                        />
                    <!-- <textarea name="sentense" cols="30" rows="10" class="form-control" :class="{'is-invalid': errors.sentense}" v-model="questionGroup.sentense" placeholder="問題グループ本文" required></textarea> -->
                    <div id="validationSentenseFeedback" class="invalid-feedback" v-if="errors.sentense">{{ errors.sentense }}</div>
                </div>

                <div class="row">
                    <div class="mb-3 col-12 col-md-6">
                        <label class="form-label" for="chapter_id">Chapter</label>
                        <select class="form-select" name="chapter_id" data-width="100%" tabindex="null" @change.prevent="selectedChapter">
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
                            <input type="text" name="title" class="form-control" :class="{'is-invalid': errors.title}" v-model="question.title" placeholder="タイトル" required>
                            <div id="validationTitleFeedback" class="invalid-feedback" v-if="errors.title">{{ errors.title }}</div>
                        </div>
                    </div>

                    <div class="mb-12 col-12 col-md-12">
                        <label class="form-label" for="sentense">Sentense</label>
                        <quill-editor
                            v-model='question.sentense'
                            ref='textEditor'
                            :options='editorOption'
                            class="from-control"
                            :class="{'is-invalid': errors.sentense}"
                        />
                        <!-- <textarea name="sentense" cols="30" rows="10" class="form-control" :class="{'is-invalid': errors.sentense}" v-model="question.sentense" placeholder="問題本文" required></textarea> -->
                        <div id="validationSentenseFeedback" class="invalid-feedback" v-if="errors.sentense">{{ errors.sentense }}</div>
                    </div>

                    <div class="row">
                        <div class="custom-file mb-3 col-12 col-md-6">
                            <label class="form-label" for="image">Figure (Option)</label>
                            <input type="file" class="form-control custom-file-input" name="image" @change.prevent="changeImage($event, question, 'image')">
                        </div>
                    </div>

                    <hr class="my-5">

                    <!-- 回答選択肢 -->
                    <h4 class="mb-0">Selections</h4>
                    <p class="mb-4">回答選択肢 (4つ)</p>

                    <div class="row">
                        <AnswerForm :answer="answer" :key="answer.index" v-for="answer in question.answers" />
                    </div>

                    <div class="row">
                        <div class="mb-3 col-12 col-md-6">
                            <label class="form-label" for="correct_index">Correct Answer</label>
                            <select class="form-select" name="correct_index" data-width="100%" tabindex="null" v-model="question.correct_index" required>
                                <option :value="answer.index" :key="answer.index" v-for="answer in question.answers">選択肢{{ answer.index }}</option>
                            </select>
                        </div>
                    </div>

                    <div class="col-12">
                        <button class="btn btn-secondary"  @click.prevent="question.addNewAnswer()">Add Selection</button>
                    </div>

                    <hr class="my-5">

                    <!-- 解説文 -->
                    <h4 class="mb-0">Answer Commentary</h4>
                    <p class="mb-4">正解の選択肢についての解説</p>
                    
                    <div class="mb-3 col-12 col-md-12">
                        <label class="form-label" for="commentary">Commentary</label>
                        <quill-editor
                            v-model='question.commentary'
                            ref='textEditor'
                            :options='editorOption'
                            class="from-control"
                            :class="{'is-invalid': errors.commentary}"
                        />
                        <div id="validationCommentaryFeedback" class="invalid-feedback" v-if="errors.commentary">{{ errors.commentary }}</div>
                    </div>

                    <div class="custom-file mb-3 col-12 col-md-6">
                        <label class="form-label" for="chapter_id">Figure (Option)</label>
                        <input type="file" class="form-control custom-file-input" name="commentary_image" @change.prevent="changeImage($event, question, 'commentary_image')">
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

    <!-- 画像編集モーダル -->
    <image-crop-modal :file="editingImage.file" :data="editingImage.data" v-if="editingImage.data" @crop="finishChangeImage" @cancel="cancelChangeImage" />
</div>
</template>


<script lang="js">
import draggable from 'vuedraggable';

import QuestionGroup from '../models/QuestionGroup';
import Question from '../models/Question';
import AnswerForm from '../components/AnswerForm';
import QuestionGroupAPI from '../apis/QuestionGroupAPI';

import ImageCropModal from '../components/ImageCropModal';

export default {
    name: 'CreateQuestionGroupPage',
    components: {
        AnswerForm,
        ImageCropModal,
    },
    data: function () {
        let regex = /.*\/workbooks\/([0-9a-z\-]+)\/questions\/new_group\/+/i
        let url = window.location.href;
        let workbookId = url.match(regex)[1];
        let token = document.getElementById('token').dataset.value
        let api = new QuestionGroupAPI(token);
        return {
            workbookId: workbookId,
            api: api,
            questionGroup: new QuestionGroup(),
            editingQuestion: null,
            chapters: JSON.parse(document.getElementById('chapters').dataset.value),
            errors: {},
            editingImage: {
                file: null,
                data: null,
                type: null,
            },
            editorOption: {
                placeholder: 'What’s on your mind?',
                theme: 'snow',
                modules: {
                    markdownShortcuts: {},
                    toolbar: [
                        [{ header: [1, 2, 3, 4, 5, false] }],
                        ['blockquote', 'bold', 'italic', 'link', 'code-block']
                    ]
                }
            }
        }
    },
    beforeMount() {
        // question_group_idが指定されている場合は複製する
        let uri = window.location.search.substring(1);
        let params = new URLSearchParams(uri);
        let questionGroupId = params.get("question_group_id");
        if (questionGroupId) {
            this.api.QuestionGroupAPI(this.workbookId, questionGroupId).then(questionGroup => {
                this.questionGroup = questionGroup;
            });
        }
    },
    methods: {
        changeImage(e, question, type) {
            let file = e.target.files[0];
            let reader = new FileReader();
            let that = this;
            this.editingQuestion = question;
            reader.readAsDataURL(file);
            reader.onload = function(e) {
                let data = e.target.result;
                that.editingImage = { data, file, type };
            };
        },
        async finishChangeImage(file, width, height, left, top) {
            this.$isLoading(true);
            await this.editingQuestion.upload(this.api, file, width, height, left, top).then(url => {
                if (this.editingImage.type == 'image') {
                    this.editingQuestion.image_urls = [url];
                } else if (this.editingImage.type == 'commentary_image') {
                    this.editingQuestion.commentary_image_urls = [url];
                }
                this.editingImage = {
                    data: null,
                    file: null,
                    type: null,
                }
            }).finally(() => {
                this.$isLoading(false);
            });
        },
        cancelChangeImage() {
            this.editingImage = {
                data: null,
                file: null,
                type: null,
            }
        },
        addQuestion() {
            this.questionGroup.addNewQuestion();
        },
        selectedChapter(e) {
            this.questionGroup.setChapter(e.target.value)
        },
        async createQuestionGroup() {
            this.api.createQuestionGroup(this.workbookId, this.questionGroup).then(data => {
                window.location.href = window.location.href.replace('/questions/new_group', '');
            }).catch(error => {
                this.errors = {};
                for (let e of error.data.errors) {
                    this.errors[e.field] = e.message;
                }
            })
        }
    },
}
</script>