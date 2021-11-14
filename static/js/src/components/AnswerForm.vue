<template>
    <div class="mb-3 col-12 col-md-6">
        <div class="mb-3 col-12 col-md-12">
            <label class="form-label" for="sentense" style="width: 100%;">
                ({{ answer.index }})
                <span class="dropdown dropstart" style="float: right;">
                    <a class="text-muted text-decoration-none" href="#" role="button" :id="`question-menu-${answer.index}`" data-bs-toggle="dropdown" data-bs-offset="-20,20" aria-expanded="false">
                        <i class="fe fe-more-vertical"></i>
                    </a>
                    <span class="dropdown-menu" :aria-labelledby="`question-menu-${answer.index}`" style="">
                        <a class="dropdown-item" @click.prevent="onClickDelete(answer.index)"><i class="fe fe-edit dropdown-item-icon"></i>削除</a>
                    </span>
                </span>
            </label>
            <input type="text" v-model="answer.sentense" name="sentense" class="form-control" placeholder="回答選択肢" required />
        </div>
    </div>
</template>


<script lang="js">

import Answer from '../models/Answer';

export default {
    name: 'AnswerForm',
    props: {
        answer: Answer,
    },
    components: {
    },
    async beforeMount() {
    },
    methods: {
        onClickDelete(index) {
            this.$emit('clickDelete', index);
        }
    },
}
</script>