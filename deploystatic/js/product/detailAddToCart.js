$( ".add_to_cart_button" ).click(function(e) {
  e.preventDefault();
  let select_variation = document.getElementById( "select-variation" );
  let variation_id =( select_variation.options[ select_variation.selectedIndex ].value )
  try {
  let quantity = document.getElementById('quantity').value;
} catch (exceptionVar) {
   let quantity = 1
}
    //  let quantity = document.getElementById("quantity").getAttribute("data-quantity");
  var max_stock =document.getElementById("quantity").getAttribute("data-max-quantity");
  if (quantity === undefined || quantity == null || quantity <= 0){
    quantity = 1
  } 
  if (quantity >max_stock){
    quantity = max_stock;
  }
  $.ajax({
    type: "POST",
    url: url_dynamic_add_to_cart_button,
    data: {
        variationid: variation_id,
        productquantity: quantity,
        csrfmiddlewaretoken: csrf_token,
        action: 'cart_add'
    },
    success: (json) => {
      console.log(json)}
      
       //document.getElementById("cart-quantity").innerHTML = json.quantity}
      /*,
    error: function (xhr, errmsg, err) {
        console.log(xhr,errmsg,err)
    }*/
  });

})
