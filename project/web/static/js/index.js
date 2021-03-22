$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
  if (!$(this).next().hasClass('show')) {
    $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
  }
  var $subMenu = $(this).next(".dropdown-menu");
  $subMenu.toggleClass('show');


  $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
    $('.dropdown-submenu .show').removeClass("show");
  });


  return false;
});
$(function(){

    $(window).bind('beforeunload', triggerClose)



    $("#test").bind("click",triggerClose)
    
    
    function triggerClose(e){
        var url = document.location.origin + '/close'
        var data = {}
        var items = Object.entries(e)
        for(var i =0 ;i<items.length; i++){
            var item = items[i]
            var key = item[0]
            var value = item[1]
            data[key] = value
        }
        document.getElementById("close").innerText = "Hello"
        console.log(data)
        var event = JSON.stringify(data)
        console.log(data)
        $.getJSON(url, {'event': event }, function(response){
            console.log(response.result)

        })
    }

})