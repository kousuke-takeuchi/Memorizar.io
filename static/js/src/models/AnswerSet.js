import Answer from "./Answer";

export default class AnswerSet {
    constructor(size) {
        this.size = size;
        this.answers = new Array();
        for (var i = 0; i < size; i++) {
            var index = i + 1;
            this.answers.push(new Answer(index));
        }
    }

    addNewAnswer() {
        var index = this.size;
        this.answers.push(new Answer(index));
        this.size++;
    }

    deleteAnswer(index) {
        if (this.size > 0) {
            this.answers = this.answers.splice(index);
            this.size--;

            for (var i = 0; i < this.size; i++) {
                var index = i + 1;
                this.answers[i].index = index
            }
        }
    }
}