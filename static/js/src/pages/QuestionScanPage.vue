<template>
<!-- 問題作成フォーム -->
<div class="container pt-5 pb-5">
    <div class="lg-12 md-12 col-12"> 
        <div class="card">
            <div class="d-lg-flex justify-content-between align-items-center card-header">
                <div class="mb-3 mb-lg-0">
                    <h3 class="mb-0">Scan a Question</h3>
                    <span>問題のスキャン</span>
                </div>

                <button v-if="status == 'reading'" class="btn btn-primary" type="button" disabled>
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="sr-only">読み取り中...</span>
                </button>
                <button v-else class="btn btn-success" @click.prevent="takeSnapshot">読み取り開始</button>

            </div>

            <div class="card-body">
                <div ref="canvas-container" style="width:100%;margin:0 auto;">
                    <canvas ref="canvas"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>
</template>


<script lang="js">
import Tesseract from 'tesseract.js';

import Question from '../models/Question';
import QuestionAPI from '../apis/QuestionAPI';

var image = null;

export default {
    name: 'QuestionScanPage',
    components: {
    },
    data: function () {
        let regex = /.*\/workbooks\/([0-9a-z\-]+)\/questions\/new\/+/i
        let url = window.location.href;
        let workbookId = url.match(regex)[1];
        let token = document.getElementById('token').dataset.value
        let api = new QuestionAPI(token);
        return {
            workbookId: workbookId,
            api: api,
            question: new Question(),
            chapters: JSON.parse(document.getElementById('chapters').dataset.value),
            errors: {},

            video: null,
            canvas: null,
            context: null,
            dataUrl: '',
            status: 'none'
        }
    },
    async mounted() {
        this.status = 'initialize';
        
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({video: true}).then((stream)=>{
                // this.$refs.videoRef.srcObject = stream;
                this.canvas = this.$refs.canvas;
                this.context = this.canvas.getContext('2d');

                this.video = document.createElement('video');
                this.video.addEventListener('loadedmetadata', () => {
                    // メタデータが取得できるようになったら実行
                    const canvasContainer = this.$refs['canvas-container'];
                    this.canvas.width = canvasContainer.offsetWidth;
                    this.canvas.height = parseInt(this.canvas.width * this.video.videoHeight / this.video.videoWidth);
                    this.render();
                });
                // iOSのために以下３つの設定が必要
                this.video.setAttribute('autoplay', '');
                this.video.setAttribute('muted', '');
                this.video.setAttribute('playsinline', '');
                this.video.srcObject = stream;
                this.playVideo();
            });
        }
    },
    methods: {
        render() {
            if(this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
                this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            }
            requestAnimationFrame(this.render);
        },
        async runOcr() {
            this.status = 'reading';

            return Tesseract.recognize(this.dataUrl, 'jpn', {
                // logger: log => {
                //     console.log(log);
                // }
            })
            .then(result => {
                alert(result.data.text);
            })
            .catch(error => console.log(error))
            .finally(() => {
                this.playVideo();
            });
        },
        playVideo() {
            this.video.play();
            this.status = 'play';
        },
        pauseVideo() {
            this.video.pause();
            this.status = 'pause';
        },
        takeSnapshot() {
            this.pauseVideo();
            this.dataUrl = this.canvas.toDataURL();
            this.runOcr();
        },
    },
}
</script>