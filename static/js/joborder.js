$(document).ready(function () {
  function calculateTotal() {
    const serviceFee = parseFloat($("#serviceFee").val()) || 0;
    const parts = parseFloat($("#parts").val()) || 0;
    const total = serviceFee + parts;

    $("#total").val(total.toFixed(2));
  }

  $("#serviceFee").on("input", () => calculateTotal());
  $("#parts").on("input", () => calculateTotal());
  calculateTotal();
});
