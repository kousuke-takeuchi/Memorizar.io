<template>
<div>
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
                    <!-- 問題 -->
                    <h4 class="mb-0">Question</h4>
                    <p class="mb-4">共通項目の編集</p>

                    <div class="row">
                        <div class="mb-3 col-12 col-md-6">
                            <label class="form-label" for="chapter_id">Chapter</label>
                            <select class="form-select" name="chapter_id" data-width="100%" tabindex="null" v-model="chapter_id">
                                <!-- <option value="" selected disabled>チャプターを選択してください</option> -->
                                <option :value="chapter.chapter_id" :key="chapter.chapter_id" v-for="chapter in chapters">{{ chapter.title }}</option>
                            </select>
                        </div>
                    </div>

                    <hr class="my-5">

                    <div class="custom-file mb-3 col-12 col-md-6">
                        <label class="form-label" for="image">問題画像</label>
                        <input type="file" class="form-control custom-file-input" name="image" @change.prevent="changeImage($event, 'image')">
                    </div>

                    <div class="preview col-12 col-md-12">
                        <img class="preview-image" src="http://placehold.jp/1024x720.png" />
                        <svg :viewBox="viewBox" class="label-area" id="annotation1" @mousedown="startDrawingBox($event, 'annotation1')" @mousemove="changeBox($event, 'annotation1')" @mouseup="stopDrawingBox">
                            <g v-if="drawingBox">
                                <rect :stroke="color(true)" fill-opacity="0%" stroke-width="5" :height="drawingBox.height" :width="drawingBox.width" :y="drawingBox.y" :x="drawingBox.x" />
                            </g>
                            <g :key="index" v-for="(questionBoundingBox, index) in questionBoundingBoxes">
                                <text :x="questionBoundingBox.bbox.x" :y="questionBoundingBox.bbox.y-5" font-size="1.5em" font-weight="bold" :fill="color(false)" >
                                    {{ index + 1 }}
                                </text>
                                <rect :stroke="color(false)" fill-opacity="0%" stroke-width="5" :height="questionBoundingBox.bbox.height" :width="questionBoundingBox.bbox.width" :y="questionBoundingBox.bbox.y" :x="questionBoundingBox.bbox.x" />
                            </g>
                        </svg>
                    </div>

                    <hr class="my-5">

                    <!-- 回答選択肢 -->
                    <h4 class="mb-0">Questions</h4>
                    <p class="mb-4">問題の編集</p>

                    <bulk-question-form :index="index+1" :question="questionBoundingBox.question" :key="index" v-for="(questionBoundingBox, index) in questionBoundingBoxes" />

                    <hr class="my-5">

                    <div class="custom-file mb-3 col-12 col-md-6">
                        <label class="form-label" for="commentary_image">解説画像</label>
                        <input type="file" class="form-control custom-file-input" name="commentary_image" @change.prevent="changeImage($event, 'commentary_image')">
                    </div>

                    <div class="preview col-12 col-md-12">
                        <img class="preview-image" src="http://placehold.jp/1024x720.png" />
                        <svg :viewBox="viewBox" class="label-area" id="annotation2" @mousedown="startDrawingBox($event, 'annotation2')" @mousemove="changeBox($event, 'annotation2')" @mouseup="stopCommentaryDrawingBox">
                            <g v-if="drawingBox">
                                <rect :stroke="color(true)" fill-opacity="0%" stroke-width="5" :height="drawingBox.height" :width="drawingBox.width" :y="drawingBox.y" :x="drawingBox.x" />
                            </g>
                            <g :key="index" v-for="(commentaryBoundingBox, index) in commentaryBoundingBoxes">
                                <text :x="commentaryBoundingBox.bbox.x" :y="commentaryBoundingBox.bbox.y-5" font-size="1.5em" font-weight="bold" :fill="color(false)" >
                                    {{ index + 1 }}
                                </text>
                                <rect :stroke="color(false)" fill-opacity="0%" stroke-width="5" :height="commentaryBoundingBox.bbox.height" :width="commentaryBoundingBox.bbox.width" :y="commentaryBoundingBox.bbox.y" :x="commentaryBoundingBox.bbox.x" />
                            </g>
                        </svg>
                    </div>

                    <!-- 送信ボタン -->
                    <div class="col-12">
                        <button class="btn btn-primary" @click.prevent="createQuestions">Create Questions</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>


<script lang="js">
import Question from '../models/Question';
import QuestionAPI from '../apis/QuestionAPI';

import BulkQuestionForm from '../components/BulkQuestionForm';

export default {
    name: 'CreateQuestionPage',
    components: {
        BulkQuestionForm,
    },
    data: function () {
        let regex = /.*\/workbooks\/([0-9a-z\-]+)\/questions\/new_bulk\/+/i
        let url = window.location.href;
        let workbookId = url.match(regex)[1];
        let defaultAnswerCount = document.getElementById('default_answer_count').dataset.value
        let token = document.getElementById('token').dataset.value
        let api = new QuestionAPI(token);
        return {
            workbookId: workbookId,
            api: api,
            chapters: JSON.parse(document.getElementById('chapters').dataset.value),
            chapter_id: null,
            questionBoundingBoxes: [],
            commentaryBoundingBoxes: [],
            errors: {},
            drawingBox: null,
            editingImage: {
                width: 1024,
                height: 720,
            },
        }
    },
    computed: {
        viewBox() {
            return `0 0 ${this.editingImage.width} ${this.editingImage.height}`; 
        },
    },
    methods: {
        changeImage(e, type) {
            this.editingImage.loaded = false;
            
            let file = e.target.files[0];
            if(!file || file.type.indexOf('image/') !== 0)
                return;
            
            let reader = new FileReader();
            
            reader.readAsDataURL(file);
            reader.onload = function (evt) {
                let img = new Image();
                img.onload = () => {
                    this.editingImage.width = img.width;
                    this.editingImage.height = img.height;
                    this.editingImage.loaded = true;
                }
                img.src = evt.target.result;
            }

            reader.onerror = evt => {
                console.error(evt);
            }
        },
        startDrawingBox(e, id) {
            this.drawingBox = {
                width: 0,
                height: 0,
                y: this.getCoursorTop(e, id),
                x: this.getCoursorLeft(e, id),
            };
        },
        changeBox(e, id) {
            if (this.drawingBox) {
                var width = this.getCoursorLeft(e, id) - this.drawingBox.x;
                var height = this.getCoursorTop(e, id) - this.drawingBox.y;
                if (width > 0 && height > 0) {
                    this.drawingBox = {
                        ...this.drawingBox,
                        width: this.getCoursorLeft(e, id) - this.drawingBox.x,
                        height: this.getCoursorTop(e, id) - this.drawingBox.y,
                    };
                }
            }
        },
        stopDrawingBox() {
            if (this.drawingBox && this.drawingBox.width > 5) {
                let bbox = {
                    x: this.drawingBox.x,
                    y: this.drawingBox.y,
                    width: this.drawingBox.width,
                    height: this.drawingBox.height,
                }
                this.questionBoundingBoxes.push({question: new Question(4), bbox: bbox})
            }
            this.drawingBox = null;
        },
        stopCommentaryDrawingBox() {
            if (this.drawingBox && this.drawingBox.width > 5) {
                let bbox = {
                    x: this.drawingBox.x,
                    y: this.drawingBox.y,
                    width: this.drawingBox.width,
                    height: this.drawingBox.height,
                }
                this.commentaryBoundingBoxes.push({bbox: bbox})
            }
            this.drawingBox = null;
        },
        getWidthRate(id) {
            const rect = document.getElementById(id).getBoundingClientRect();
            return this.editingImage.width / rect.width;
        },
        getHeightRate(id) {
            const rect = document.getElementById(id).getBoundingClientRect();
            return this.editingImage.height / rect.height;
        },
        getCoursorLeft(e, id) {
            const rect = document.getElementById(id).getBoundingClientRect();
            return Math.round((e.clientX - rect.left) * this.getWidthRate(id));
        },
        getCoursorTop(e, id) {
            const rect = document.getElementById(id).getBoundingClientRect();
            return Math.round((e.clientY - rect.top) * this.getHeightRate(id));
        },
        color(flag) {
            return flag ? "#dc3545" : "#ffc107"
        },
        async createQuestions() {
            this.api.createQuestions(this.workbookId, this.question).then(data => {
                window.location.href = window.location.href.replace('/questions/new', '');
            }).catch(error => {
                console.log(error)
                this.errors = {};
                for (let e of error.data.errors) {
                    this.errors[e.field] = e.message;
                }
            })
        }
    },
}
</script>

<style scoped>
  .preview {
    position: relative;
  }
  .preview-image {
    width: 100%;
  }
  .label-area {
      position: absolute;
      top: 1.25rem;
      bottom: 1.25rem;
      left: 1.25rem;
      right: 1.25rem;
  }
  .class-badge {
    margin: 5px;
  }
  .remove-descriptor-btn {
    position: absolute;
    right: 30px;
    bottom: 15px;
  }
</style>