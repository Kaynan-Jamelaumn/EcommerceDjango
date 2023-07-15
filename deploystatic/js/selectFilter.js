  $("#select-filter").change(function (e) {
    e.preventDefault();
    let filter = document.getElementById("select-filter").value

    $.ajax({
      type: 'POST',
      url: "{% url 'product:select-filter' %}",
      data: {
        filter: filter,
        csrfmiddlewaretoken: csrf_token,
        action: 'select-filter'
      },
    });
  });