import openpyxl

from django.utils import timezone

from workbooks import models


class WorkbookService:
    def import_workbook(self, user, filename):
        wb = openpyxl.load_workbook(filename)
        sheet = wb.worksheets[0]

        default_title = '問題集 ' + timezone.now().strftime('%Y%m%d-%H%M%S')
        # workbook = models.Workbook.objects.all().first()
        workbook = models.Workbook.objects.create(user=user, title=default_title)
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
                current_capter, created = models.Chapter.objects.get_or_create(
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