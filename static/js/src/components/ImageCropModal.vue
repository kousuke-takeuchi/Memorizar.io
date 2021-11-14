<template>
    <div id="image-crop-editor">
        <button id="close" type="button" class="btn-close" aria-label="Close"></button>
        <cropper :src="data" @change="change" />
        <button id="submit" type="button" class="btn btn-success" @click.prevent="finish">完了</button>
    </div>  
</template>


<script lang="js">
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';

export default {
    name: 'ImageCropModal',
    components: {
		Cropper,
	},
    props: {
        file: {
            type: File,
            required: true,
        },
        data: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            coordinates: null,
        }
    },
    methods: {
        change({ coordinates, canvas }) {
            this.coordinates = coordinates;
		},
        finish() {
            let { width, height, left, top } = this.coordinates;
            this.$emit('crop', this.file, width, height, left, top);
        },
    },
}
</script>


<style scoped>
#image-crop-editor {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: 100;
}

#image-crop-editor #close {
    position: fixed;
    left: 10px;
    top: 10px;
    width: 25px;
    height: 25px;
    z-index: 101;
}

#image-crop-editor #submit {
    position: fixed;
    right: 10px;
    top: 10px;
    z-index: 101;
}
</style>