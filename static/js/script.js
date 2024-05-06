$(window).on('scroll', function() {
    var scroll = $(window).scrollTop();
  
    console.log(scroll > 100);
  
    if (scroll) {
      $('nav').removeClass('nav-fade');
      $('nav').addClass('nav-show');
    }
  
    else {
      $('nav').removeClass('nav-show');
      $('nav').addClass('nav-fade')
    }
  })
  
  function nav() {
    document.getElementById("navbar").classList.toggle("nav-open");
  }