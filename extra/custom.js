$(document).ready(function(){
   var flag = true;
   $('img[alt=preview]').click(function() {
       $(this).stop().animate({width: (flag ? "100%" : "40%") }, 'fast');
       flag = !flag;
   });
});
