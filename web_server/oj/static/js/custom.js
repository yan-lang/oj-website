$(document).ready(function () {
    $("button.grade-expand").click(function () {
        if($(this).attr("aria-expanded") === "true") {
            $(this).children("svg.bi-chevron-down").hide()
            $(this).children("svg.bi-chevron-right").show()
        } else {
            $(this).children("svg.bi-chevron-right").hide()
            $(this).children("svg.bi-chevron-down").show()
        }
    })
});