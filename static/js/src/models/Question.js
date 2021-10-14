import Answer from './Answer';


export default class Question {
    constructor(size) {
        this.question_id = null;
        this.title = null;
        this.sentense = null;
        this.chapter_id = null;
        this.chapter = null;
        this.correct_index = null;
        this.commentary = null;
        
        if (size === undefined) {
            size = 4;
        }
        this.size = size;
        this.answers = new Array();
        for (var i = 0; i < size; i++) {
            var index = i + 1;
            this.answers.push(new Answer(index));
        }
    }

    addNewAnswer() {
        var index = this.size;
        this.answers.push(new Answer(index+1));
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