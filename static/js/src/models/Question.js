import Answer from './Answer';


class Question {
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

    reindex() {
        for (var i = 0; i < this.size; i++) {
            var index = i + 1;
            this.answers[i].index = index;
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

    selectAnswer(answerId) {
        for (var answer of this.answers) {
            answer.selected = false;
            if (answer.answer_id == answerId) {
                answer.selected = true;
            }
        }
    }
}


Question.load_data = function (question_data, answers_data) {
    const question = new Question(answers_data.length);
    question.question_id = question_data.question_id;
    question.sentense = question_data.sentense;
    question.image_urls = question_data.image_urls;

    question.answers = [];
    for (var answer_data of answers_data) {
        const answer = new Answer(answer_data.index);
        answer.answer_id = answer_data.answer_id;
        answer.title = answer_data.title;
        answer.sentense = answer_data.sentense;
        question.answers.push(answer);
    }

    return question;
}

export default Question;