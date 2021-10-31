import random
import datetime
import openpyxl

from django.core.mail import send_mail
from django.template.loader import render_to_string

from workbooks import models


class WorkbookService:
    def import_workbook(self, user, title, filename):
        wb = openpyxl.load_workbook(filename)
        sheet = wb.worksheets[0]

        workbook = models.Workbook.objects.create(user=user, title=title)
        current_capter = None
        relationships = []
        for idx, row in enumerate(sheet.rows):
            if idx == 0:
                continue

            # チャプターが指定されている場合は作成
            chapter_id = row[0].value # チャプター(章)識別子
            chapter_title = row[1].value # チャプター名
            chapter_description = row[2].value # チャプター詳細
            if chapter_id:
                current_capter, _ = models.Chapter.objects.get_or_create(
                    workbook=workbook,
                    chapter_id=chapter_id,
                    title=chapter_title,
                    description=chapter_description,
                )

            # 問題集を作成
            question_id = row[3].value # 問題識別子
            question_title = row[4].value # 問題タイトル
            question_sentense = row[5].value # 問題文章
            question_image_url = row[6].value # 問題挿入画像URL
            question_hint = row[7].value # 問題ヒント文章
            commentary = row[32].value # 答え解説文章(強調や色の機能つけたい)
            commentary_image_url = row[33].value # 答え解説画像URL
            question, created = models.Question.objects.get_or_create(
                question_id=question_id,
                chapter=current_capter,
                workbook=workbook,
                title=question_title,
                sentense=question_sentense,
                image_urls=[question_image_url] if question_image_url else [],
                hint=question_hint,
                commentary=commentary,
                commentary_image_urls=[commentary_image_url] if commentary_image_url else [],
            )

            # 正解の選択肢
            true_answers = [
                row[24].value, # 答え1
                row[25].value, # 答え2(複数時)
                row[26].value, # 答え3(複数時)
                row[27].value, # 答え4(複数時)
                row[28].value, # 答え5(複数時)
                row[29].value, # 答え6(複数時)
                row[30].value, # 答え7(複数時)
                row[31].value, # 答え8(複数時)
            ]
            true_answers = [ta for ta in true_answers if ta]

            # is_true必要
            answer1_title = row[8].value # 回答選択肢1名称
            answer1_sentense = row[9].value # 回答選択肢1文章
            if answer1_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer1_title,
                    sentense=answer1_sentense,
                    is_true=(answer1_title in true_answers),
                )

            answer2_title = row[10].value # 回答選択肢2名称
            answer2_sentense = row[11].value # 回答選択肢2文章
            if answer2_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer2_title,
                    sentense=answer2_sentense,
                    is_true=(answer2_title in true_answers),
                )

            answer3_title = row[12].value # 回答選択肢3名称
            answer3_sentense = row[13].value # 回答選択肢3文章
            if answer3_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer3_title,
                    sentense=answer3_sentense,
                    is_true=(answer3_title in true_answers),
                )

            answer4_title = row[14].value # 回答選択肢4名称
            answer4_sentense = row[15].value # 回答選択肢4文章
            if answer4_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer4_title,
                    sentense=answer4_sentense,
                    is_true=(answer4_title in true_answers),
                )

            answer5_title = row[16].value # 回答選択肢5名称
            answer5_sentense = row[17].value # 回答選択肢5文章
            if answer5_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer5_title,
                    sentense=answer5_sentense,
                    is_true=(answer5_title in true_answers),
                )

            answer6_title = row[18].value # 回答選択肢6名称
            answer6_sentense = row[19].value # 回答選択肢6文章
            if answer6_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer6_title,
                    sentense=answer6_sentense,
                    is_true=(answer6_title in true_answers),
                )

            answer7_title = row[20].value # 回答選択肢7名称
            answer7_sentense = row[21].value # 回答選択肢7文章
            if answer7_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer7_title,
                    sentense=answer7_sentense,
                    is_true=(answer7_title in true_answers),
                )

            answer8_title = row[22].value # 回答選択肢8名称
            answer8_sentense = row[23].value # 回答選択肢8文章
            if answer8_title:
                models.Answer.objects.get_or_create(
                    question=question,
                    title=answer8_title,
                    sentense=answer8_sentense,
                    is_true=(answer8_title in true_answers),
                )
            
            relative_question1_id = row[34].value # 類似問題1
            if relative_question1_id:
                relationships.append((question, relative_question1_id))
            relative_question2_id = row[35].value # 類似問題2
            if relative_question2_id:
                relationships.append((question, relative_question2_id))
            relative_question3_id = row[36].value # 類似問題3
            if relative_question3_id:
                relationships.append((question, relative_question3_id))
            relative_question4_id = row[37].value # 類似問題4
            if relative_question4_id:
                relationships.append((question, relative_question4_id))
        
        # 問題の関連を作成
        for r in relationships:
            question1 = r[0]
            question2 = models.Question.objects.get(question_id=r[1])
            models.Relationship.objects.get_or_create(
                question1=question1,
                question2=question2,
            )
    
    def get_chapters(self, workbook):
        chapters = workbook.chapter_set.all()
        chapters_data = {}
        for chapter in chapters:
            training_count = models.TrainingSelection.objects.filter(question__chapter=chapter).count()
            training_question_count = models.TrainingSelection.objects.filter(question__chapter=chapter).distinct('question').count()
            question_count = models.Question.objects.filter(workbook=workbook).count()
            correct_count = models.TrainingSelection.objects.filter(question__chapter=chapter, correct=True).count()

            # 実施回数
            learning_count = models.TrainingSelection.objects.filter(question__chapter=chapter).distinct('training').count()
            # 実施率 = 実施回数 / 問題数
            if question_count > 0:
                training_rate = training_question_count / question_count
            else:
                training_rate = 0
            # 正解率 = 正解数 / 実施回数
            if training_count:
                correct_rate = correct_count / training_count
            else:
                correct_rate = 0

            chapters_data[chapter] = {
                'learning_count': learning_count,
                'training_rate': round(training_rate*100),
                'correct_rate': round(correct_rate*100),
            }
        return chapters_data


    def aggregate_daily(self, workbook):
        # 最近7日の1日ごとの学習回数と正解数を集計
        learning_counts = []
        correct_counts = []
        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]
        for date in dates:
            trainings = models.Training.objects.filter(workbook=workbook, created_at__range=[datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)])
            learning_count = models.TrainingSelection.objects.filter(training__in=trainings).distinct('training').count()
            correct_count = models.TrainingSelection.objects.filter(training__in=trainings, correct=True).count()
            learning_counts.append(learning_count)
            correct_counts.append(correct_count)
        weeks = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        dates = [weeks[date.weekday()] for date in dates]
        return (dates, learning_counts, correct_counts)
    

    def get_wrong_question(self, workbook, current_question_id=None):
        wrong_questions = []
        for selection in models.TrainingSelection.objects.filter(training__workbook=workbook, correct=False):
            if not selection.question in wrong_questions:
                wrong_questions.append(selection.question)
        
        if current_question_id:
            current_question = models.Question.objects.get(question_id=current_question_id)
            current_question_idx = None
            for idx, question in enumerate(wrong_questions):
                if current_question.question_id == question.question_id:
                    current_question_idx = idx
                    break
            wrong_questions = wrong_questions[current_question_idx:]
        
        if len(wrong_questions) > 1:
            return wrong_questions[0], wrong_questions[1]
        elif len(wrong_questions) > 0:
            return wrong_questions[0], None
        else:
            return None, None

    def notify_success(self, user, title):
        # 表題
        subject = "【Memorizar】インポート結果"
        # 送信元
        from_email = "noreply@memorizar.io"
        # 送信先
        recipient_list = [user.email,]
        # パラメータ
        context = {"title": title}
        
        # テンプレート
        msg_plain = render_to_string('workbooks/mail/import_success.txt', context)
        msg_html = render_to_string('workbooks/mail/import_success.html', context)

        send_mail(subject, msg_plain, from_email, recipient_list, html_message=msg_html)


    def notify_failure(self, user, title):
        # 表題
        subject = "【Memorizar】インポート結果"
        # 送信元
        from_email = "noreply@memorizar.io"
        # 送信先
        recipient_list = [user.email,]
        # パラメータ
        context = {"title": title}
        
        # テンプレート
        msg_plain = render_to_string('workbooks/mail/import_failure.txt', context)
        msg_html = render_to_string('workbooks/mail/import_failure.html', context)

        send_mail(subject, msg_plain, from_email, recipient_list, html_message=msg_html)


class TrainingService:
    def select_questions(self, training):
        # ORMでSQL発行すると副クエリが大量に発生するため、
        # 1問題集に含まれる問題数はさほど多くないので、pythonのリストでフィルター処理する

        if training.training_type == models.Training.TrainingTypes.SELECT_CHAPTER:
            # チャプターを指定する場合は、選ばれたチャプターの中から問題を取得
            chapters = training.chapters.all()
            questions = models.Question.objects.filter(workbook=training.workbook)
        elif training.training_type == models.Training.TrainingTypes.REVIEW_MISTAKE:
            # 選択されたチャプターから間違えた問題のみ取得
            chapters = training.chapters.all()
            wrong_selections = models.TrainingSelection.objects.filter(training__workbook=training.workbook, correct=False).order_by('question').distinct()
            questions = [wrong_selection.question for wrong_selection in wrong_selections]
        elif training.training_type == models.Training.TrainingTypes.ORDERED:
            # 選択されたチャプターから問題を順番に実行
            chapters = training.chapters.all()
            questions = models.Question.objects.filter(workbook=training.workbook).order_by('index')
        else:
            # 指定されない場合はすべてのチャプターから問題を取得
            chapters = models.Chapter.objects.filter(workbook=training.workbook)
            questions = models.Question.objects.filter(workbook=training.workbook)

        # すでに回答された問題
        print("training:", training.training_id)
        print("models.TrainingSelection.objects.filter(training=training)", models.TrainingSelection.objects.filter(training=training))
        answered_question_ids = models.TrainingSelection.objects.filter(training=training).values_list('question__question_id')
        print(models.TrainingSelection.objects.filter(training=training))
        answered_question_ids = [x[0] for x in answered_question_ids]
        print("answered_question_ids:", answered_question_ids)
        # 選択されたチャプターのID
        chapter_ids = chapters.values_list('chapter_id')
        chapter_ids = [x[0] for x in chapter_ids]

        rest_questions = []
        for question in questions:
            if not question.question_id in answered_question_ids and question.chapter.chapter_id in chapter_ids:
                rest_questions.append(question)
        print("rest_questions", rest_questions)
        return rest_questions

    def select_question(self, training):
        # まだ回答されていない問題から、ランダムに問題を取得する
        questions = self.select_questions(training)
        if len(questions) == 0:
            return None, []
        question = questions[random.randint(0, len(questions)-1)]
        answers = models.Answer.objects.filter(question=question)

        return question, answers
    
    def did_finish(self, training):
        # 問題集をすべて解き終わったかどうか
        rest_questions = self.select_questions(training)
        if len(rest_questions) == 0:
            return True
        
        # 10問解いた場合も終了
        selected_questions = models.TrainingSelection.objects.filter(training=training)
        if len(selected_questions) > 9:
            return True
        return False