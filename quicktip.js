function formatMoney(value) {
  value = Math.ceil(value * 100) / 100;
  value = value.toFixed(2);
  return "$ " + value;
}

function formatSplit(value) {
  if(value ==="1") return value + " person";
  return value + " people";
}

function update() {
  var bill = Number(document.getElementById("yourBill").value) || 0;
  var tipPercent = document.getElementById("tipInput").value;
  var split = document.getElementById("splitInput").value;

  var tipValue = bill * (tipPercent / 100);
  var tipEach = tipValue / split;
  var newBillEach = (bill + tipValue) / split;

  document.getElementById("tipPercent").innerHTML = tipPercent + "%";
  document.getElementById("tipValue").innerHTML = formatMoney(tipValue);
  document.getElementById("totalWithTip").innerHTML = formatMoney(bill + tipValue);
  document.getElementById("splitValue").innerHTML = formatSplit(split);
  document.getElementById("billEach").innerHTML = formatMoney(newBillEach);
  document.getElementById("tipEach").innerHTML = formatMoney(tipEach);
}

var container = document.getElementById("container")
container.addEventListener('input', update)