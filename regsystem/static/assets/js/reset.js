document.addEventListener("DOMContentLoaded", () => {
    const allResetInputs = document.querySelectorAll(".reset-input");
  
    const resetButton = document.getElementById('reset-button');

    // inputs
    const newPasswordInput = document.getElementById('new-password-input');

    const confirmPasswordInput = document.getElementById('confirm-password-input');
  
    function trackResetChanges() {
      // count of inputs with text
      let fieldsWithText = 0;
  
      [newPasswordInput, confirmPasswordInput].forEach((eachResetField) => {
  
        if (eachResetField.value.length > 0) {
          // update the count
          fieldsWithText += 1;

        } else {

        }
      });

      // check if the contents of the input fields matche
      let fieldContentMatches = confirmPasswordInput.value == newPasswordInput.value;

  
      // if theres data and also the inputs match
      if (fieldsWithText > 1 && fieldContentMatches){
        resetButton.disabled = false;
  
      } else {
        resetButton.disabled = true;
      }
  
    }
  
    allResetInputs.forEach((eachResetInputField) => {
        eachResetInputField.addEventListener("input", () => {
          // check if all fields have data in them
          trackResetChanges();
      });
    });
  });
  