$(document).ready(function () {
    const SINGLE_CARD_WIDTH = 500;
    let container_width = SINGLE_CARD_WIDTH * $(".scrolly-inner a").length;
    $(".scrolly-inner").css("width", container_width);
});