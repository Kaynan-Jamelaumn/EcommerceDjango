  $(".add_to_cart_button").click(function (e) {
    e.preventDefault();
    let variation_id = $(this).data("variation_id");
    $.ajax({
      type: "POST",
      url: url_add_to_cart,
      data: {
        variationid: variation_id,
        productquantity: 1,
        csrfmiddlewaretoken: csrf_token,
        action: 'cart_add'
      },
      success: (json) => {
        console.log(json)
      }

      //document.getElementById("cart-quantity").innerHTML = json.quantity}
      /*,
    error: function (xhr, errmsg, err) {
        console.log(xhr,errmsg,err)
    }*/
    });

  })