DESELEMENT = "h2,h3,h4"; //"h1,h2,h3,h4,ul,div.section p,div.highlight-python";

function strip_tags(st) {
    return st.replace(/<[^>]+>?[^<]*>/g, '');
}

$(document).ready(function() {
    $("div.body > div.section").find(DESELEMENT).each(function() {
        if (!$(this).prev("div.comment").length) {
            var cmt = $('<div class="comment"><a class="email_link" title="点击提交Issue,反馈你的意见..."></a></div>');
            $(this).before(cmt);
            cmt.offset({
                //left: $(this).parents('.section').offset().left - 10,
                left: $(this).offset().left - 10,
                top: $(this).offset().top - 5
            });
        }
    });

    $("a.email_link").hover(function() {
        if ($(this).attr("href") == null||$(this).attr("href") == '') {
            var body = $(this).parent("div.comment").next().html();
            
            body = strip_tags(body).replace(/¶/g, '');
            if (body.length > 100) {
                body = body.substring(0, 100)+"...";
            }

            $(this).attr("href"
                , "https://github.com/SAEPython/saepythondevguide/issues/new?title={文档}" + encodeURIComponent(body));
            $(this).attr("target", "_blank");
        }
    }, function(){
    });

});
