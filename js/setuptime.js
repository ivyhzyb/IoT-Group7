const timeInput1 = document.getElementById("time1");
const timeInput2 = document.getElementById("time2");
const doneButton = document.getElementById("doneButton");

doneButton.addEventListener("click", function () {
  const selectedTime1 = timeInput1.value;
  const selectedTime2 = timeInput2.value;

  // intteraction with raspberry pi

  alert(
    "Selected Time 1: " + selectedTime1 + "\nSelected Time 2: " + selectedTime2
  );
});
