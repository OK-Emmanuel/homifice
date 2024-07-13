document.addEventListener('DOMContentLoaded', function() {
    $(function () {
        $(".qtyButtons input").after('<div class="qtyInc">+</div>');
        $(".qtyButtons input").before('<div class="qtyDec">-</div>');

        $(".qtyDec, .qtyInc").on("click", function () {
            var $button = $(this);
            var oldValue = $button.siblings("input").val();
            var newVal;

            if ($button.hasClass('qtyInc')) {
                newVal = parseFloat(oldValue) + 1;
            } else {
                if (oldValue > 0) {
                    newVal = parseFloat(oldValue) - 1;
                } else {
                    newVal = 0;
                }
            }
            
            $button.siblings("input").val(newVal);
        });

        $(".qtyButtons input").on('input', function () {
            var $input = $(this);
            var newVal = parseFloat($input.val());

            if (isNaN(newVal) || newVal < 0) {
                $input.val(0);
            }
        });
    });

    $(window).on('load resize', function () {
        var panelTrigger = $('.booking-widget .panel-dropdown a');
        $('.booking-widget .panel-dropdown .panel-dropdown-content').css({
            'width': panelTrigger.outerWidth()
        });
    });
});