function updateSelectedChapterIds() {
    // すべてのchapter_idを削除
    $('#selected_chapter_ids > input').remove();
    
    // 選択されたchapter_idを保存
    var chapterIds = $('#selected_chapter_ids'); 
    $('.select_chapter:checked').each(function() {
        var chapterId = $(this).attr('name');
        console.log(chapterId)
        var newInput = chapterIds.append('<input type="hidden" name="chapter_ids" value="' + chapterId + '" />');
    });
}


$(function () {
    updateSelectedChapterIds();
    
    $('.select_chapter').on('change', function (e) {
        updateSelectedChapterIds();
    });

    $('#checkAll').on('change', function (e) {
        updateSelectedChapterIds();
    })
});