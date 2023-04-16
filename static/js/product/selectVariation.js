let script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

$("#select-variation").change(function(e){
    e.preventDefault();
  
    let variation_selected = document.getElementById("select-variation").value
    
    $.ajax({
        type: 'POST',
        url: url_dynamic_variation_on_change,
        data: {
            variation_selected: variation_selected,
            csrfmiddlewaretoken: csrf_token,
            action: 'variation_on_change'
        },
        success: function (json) {
        const carouselContainers = document.querySelectorAll('.carousel-container');

        carouselContainers.forEach(function(carouselContainer, index) {
          if (index > 0) {
             const variationId = carouselContainer.getAttribute('value');
            if (variationId == variation_selected){
              carouselContainer.classList.remove('hidden');
              carouselContainer.classList.add('show');
            }  else {
                  carouselContainer.classList.remove('show');
              carouselContainer.classList.add('hidden');
                    }
          }
        });

          document.getElementById("price").innerHTML = `Price: ${json.price}`
      
          let quantity = document.getElementById('quantity');
          if (json.stock ==0){
            quantity.disabled = true;
            quantity.style.backgroundColor = "#EB455F";
            quantity.placeholder =`No Stock Available`;
          }
          else {
            quantity.disabled = false;
            quantity.style.backgroundColor = "#5fcf80";
            quantity.placeholder =`Items in stock: ${json.stock}`;
          }
          quantity.value = "";
          quantity.setAttribute("data-max-quantity", json.stock);
          if (json.promotion_price != null) {
            document.getElementById("promotion_price").innerHTML = `Promotion Pice: ${json.promotion_price}`
    
          } else{
              document.getElementById("promotion_price").innerHTML = ""
            
          }
          document.getElementById("description").innerHTML = `${json.description}`
        },
        error: function (xhr, errmsg, err) { }
    });
});