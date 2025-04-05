function validateFullName() {
  var inputField = document.getElementById("full_name");
  var fullname = inputField.value;
  var specialCharRegex = /[!@#$%^&*(),?":{}|<>_+=\[\];'"/\\₹]/;
  var alphabeticalRegex = /[a-zA-Z]/; // Regex to match alphabetical characters

  // Check if full name is empty

  // If full name is empty, return false
  if (fullname === "") {
    document.getElementById("nameError").textContent = "Full name is required.";
    return false;
  }

  // Check if at least one alphabetical character is present
  if (!alphabeticalRegex.test(fullname)) {
    document.getElementById("nameError").textContent =
      "Name should contain at least one alphabetical character.";
    return false; // Validation fails
  }

  // Check if only alphabets, numbers, dots, and hyphens are present
  if (!/^[a-zA-Z0-9\s.-]*$/.test(fullname)) {
    document.getElementById("nameError").textContent =
      "Only alphabets, numbers, dots, and hyphens are allowed.";
    return false; // Validation fails
  }

  // Check if dot is at the beginning or end of the name
  if (fullname.startsWith(".") || fullname.endsWith(".")) {
    document.getElementById("nameError").textContent =
      "Name should not start or end with a dot.";
    return false; // Validation fails
  }

  // Split the full name into words
  var words = fullname.split(" ");

  // Capitalize the first letter of each word
  words = words.map(function (word) {
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  });

  // Join the words back into a full name
  fullname = words.join(" ");

  // Automatically convert the first letter of the first word in the input field
  inputField.value = fullname;

  // Check for maximum character limit
  if (fullname.length > 200) {
    document.getElementById("nameError").textContent =
      "Maximum character limit (200) exceeded.";
    return false; // Validation fails
  }

  // Check for space at the beginning
  if (fullname.charAt(0) === " ") {
    document.getElementById("nameError").textContent =
      "Name should not start with a space.";
    return false; // Validation fails
  }

  // Check for repeating letters
  if (/(\w)\1\1/i.test(fullname)) {
    document.getElementById("nameError").textContent =
      "Name should not have the same letter repeated three times consecutively.";
    return false; // Validation fails
  }

  // Check for special characters
  if (specialCharRegex.test(fullname)) {
    document.getElementById("nameError").textContent =
      "Name should not contain special characters.";
    return false; // Validation fails
  }

  // Clear error message if all conditions are met
  document.getElementById("nameError").textContent = "";
  return true; // Validation passes
}

function validateEmail() {
  var emailField = document.getElementById("email");
  var email = emailField.value.toLowerCase(); // Convert email to lowercase
  emailField.value = email; // Update the value of the email input field

  var emailError = document.getElementById("emailError");
  // Reset previous errors
  emailError.textContent = "";
  if (email === "") {
    emailError.textContent = "Email is required.";
    return true; // Error
  }
  // Check for space at the beginning
  if (email.charAt(0) === " ") {
    emailError.textContent = "Email should not start with a space.";
    return true; // Error
  }

  // Combine regex for comprehensive email validation
  var combinedRegex =
    /^(?=.{1,254}$)(?![.-])(?!.*[.-]{2})[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?!.*\.\.)([a-zA-Z]{2,6}|xn--[a-zA-Z0-9]+)(?<!\.)$/;
  if (!combinedRegex.test(email)) {
    emailError.textContent = "Enter a valid email address.";
    return true; // Error
  }

  if (email.length > 64) {
    emailError.textContent = "Email should not exceed 64 characters.";
    return true; // Error
  }

  return false; // No error
}

function validateMobileNumber() {
  var mobileNumberField = document.getElementById("mobile_number");
  var mobileNumberError = document.getElementById("mobileError");
  var mobileNumberValue = mobileNumberField.value;

  if (mobileNumberValue === "") {
    mobileNumberError.textContent = "Mobile number is required.";
    return;
  }
  // Check if the input contains non-numeric values
  if (!/^\d+$/.test(mobileNumberValue)) {
    mobileNumberError.textContent =
      "Mobile number should only contain numeric values.";
    mobileNumberField.value = mobileNumberValue.slice(0, -1); // Remove the last entered character
    return;
  }

  // Check if the mobile number length is within 7-15 digits
  if (mobileNumberValue.length < 7 || mobileNumberValue.length > 15) {
    mobileNumberError.textContent =
      "Mobile number should be between 7 and 15 digits.";
    return; // Error
  }

  // Check if the mobile number starts with 0
  if (!/^[1-9]/.test(mobileNumberValue)) {
    mobileNumberError.textContent =
      "Mobile number should not start with 0 digits";
    mobileNumberField.value = mobileNumberValue.slice(0, -1); // Remove the last entered character
    return;
  }

  // Clear the error if all validations pass
  mobileNumberError.textContent = "";
  return true;
}

function validateZipCode() {
  var zipCodeInput = document.getElementById("pin_code");
  var zipError = document.getElementById("pinCodeError");

  // Get the entered zip code
  var zipCode = zipCodeInput.value;

  // Check if the zip code contains only numeric values and doesn't start with 0
  if (!/^[1-9]\d*$/.test(zipCode)) {
    zipCodeInput.value = zipCode.slice(0, -1); // Remove the last entered character
    zipError.textContent =
      "Zip code should contain only numeric values and not start with 0.";
    return;
  }

  // Check if the zip code has more than 6 digits
  if (zipCode.length > 6) {
    zipCodeInput.value = zipCode.slice(0, 6); // Trim to the first 6 digits
    zipError.textContent = "Zip code should be a maximum of 6 digits.";
    return;
  }

  // Clear any previous error messages
  zipError.textContent = "";
}

function validateState() {
  var stateInput = document.getElementById("state");
  var stateError = document.getElementById("stateError");
  var stateValue = stateInput.value.trim();

  // Reset previous errors
  stateError.textContent = "";

  // Check if state is selected
  if (stateValue === "") {
    stateError.textContent = "State is required.";
    return false;
  } else {
    // If the field is not empty, clear the error message
    stateError.textContent = "";
    return true;
  }
}

function validateCity() {
  var cityInput = document.getElementById("city");
  var cityError = document.getElementById("cityError");
  var cityValue = cityInput.value.trim();

  // Reset previous errors
  cityError.textContent = "";

  // Check if city is selected
  if (cityValue === "") {
    cityError.textContent = "City is required.";
    return false;
  } else {
    // If the field is not empty, clear the error message
    cityError.textContent = "";
    return true;
  }
}

function validateCountry() {
  var countryInput = document.getElementById("country");
  var countryError = document.getElementById("countryError");
  var countryValue = countryInput.value.trim();

  // Reset previous errors
  countryError.textContent = "";

  // Check if country is selected
  if (countryValue === "") {
    countryError.textContent = "Country is required.";
    return false;
  } else {
    // If the field is not empty, clear the error message
    countryError.textContent = "";
    return true;
  }
}

function validateAddress() {
  var address = document.getElementById("address").value;
  var addressError = document.getElementById("addressError");

  // Reset previous errors
  addressError.textContent = "";

  if (address === "") {
    addressError.textContent = "Address is required";
    return true;
  }
  if (/^\s*$/.test(address)) {
    addressError.textContent = "";
    return true;
  }
  // Check if the address contains only numeric characters or spaces
  if (/^\d+(\s+\d+)*$/.test(address)) {
    addressError.textContent =
      "Address should contain characters other than numbers.";
    return false;
  }

  // Check if the address contains only special characters or spaces
  if (/^[!@#$%^&*(),.?":{}|<>_+=\[\];'"/\\₹-\s]+$/.test(address)) {
    addressError.textContent =
      "Address should contain characters other than special characters.";
    return false;
  }

  // Check if the address contains only numbers and special characters or spaces
  if (/^[\d!@#$%^&*(),.?":{}|<>_+=\[\];'"/\\₹-\s]+$/.test(address)) {
    addressError.textContent =
      "Address should contain alphanumeric characters along with special characters.";
    return false;
  }

  // Clear error message if all conditions are met
  addressError.textContent = "";
  return true;
}

function validateDateOfBirth() {
  var dobField = document.getElementById("dob");
  var dobErrorTag = document.getElementById("dobError");
  var dobValue = dobField.value.trim();

  // Reset previous errors
  dobErrorTag.textContent = "";

  // Check if a date is selected
  if (dobValue === "") {
    dobErrorTag.textContent = "Date of birth is required.";
  } else {
    // Calculate the minimum and maximum allowed dates
    var minDate = new Date();
    minDate.setFullYear(minDate.getFullYear() - 20); // Minimum age of 20 years
    var maxDate = new Date();
    maxDate.setFullYear(maxDate.getFullYear() - 100); // Maximum age of 100 years

    // Convert the date string to a Date object
    var selectedDate = new Date(dobValue);

    // Check if the selected date is within the allowed range
    if (selectedDate > minDate || selectedDate < maxDate) {
      dobErrorTag.textContent = "You must be between 20 and 100 years old.";
    }
  }
}
function validateDoctorId() {
  var doctorIdImageInput = document.getElementById("doctor_id_image");
  var doctorIdErrorTag = document.getElementById("doctorIdImageError");

  doctorIdErrorTag.textContent = "";

  if (doctorIdImageInput.files.length === 0) {
    doctorIdErrorTag.textContent = "Doctor ID image is required.";
  }
}
function validateDoctorSpecialization() {
  var specializationInput = document.getElementById("selected_specialization");
  var specializationErrorTag = document.getElementById("specializationError");
  var specializationValue = specializationInput.value.trim();

  specializationErrorTag.textContent = "";

  if (specializationValue === "") {
    specializationErrorTag.textContent =
      "Specialization selection is required.";
  }
}
function validateDoctorCertificate() {
  var doctorCertificateInput = document.getElementById("doctor_certificate");
  var doctorCertificateErrorTag = document.getElementById(
    "doctorCertificateError"
  );

  doctorCertificateErrorTag.textContent = "";

  if (doctorCertificateInput.files.length === 0) {
    doctorCertificateErrorTag.textContent = "Doctor certificate is required.";
  }
}

function validateProofofWorking() {
  var proofOfWorkingInput = document.getElementById("proof_of_working");
  var doctorCertificateErrorTag = document.getElementById(
    "proofOfWorkingError"
  );
  proofOfWorkingError.textContent = "";

  if (proofOfWorkingInput.files.length === 0) {
    doctorCertificateErrorTag.textContent = "Proof of working is required.";
  }
}

function validateDateOfBirthPatient() {
  var dobField = document.getElementById("dob");
  var dobErrorTag = document.getElementById("dobError");
  var dobValue = dobField.value.trim();

  // Reset previous errors
  dobErrorTag.textContent = "";

  // Check if a date is selected
  if (dobValue === "") {
    dobErrorTag.textContent = "Date of birth is required.";
  }
}

function validateImageSize(inputId, errorId, maxSizeMB) {
  var imageUploadInput = document.getElementById(inputId);
  var imageUploadError = document.getElementById(errorId);

  if (imageUploadInput.files.length > 0) {
    // Check if the file type is an image
    var validImageTypes = [
      "image/jpeg",
      "image/png",
      "image/jpg",
      "image/bmp",
      "image/webp",
      "application/pdf",
      "image/svg+xml",
    ];
    var fileType = imageUploadInput.files[0].type;

    if (!validImageTypes.includes(fileType)) {
      imageUploadInput.value = ""; // Clear the selected file
      imageUploadError.textContent = "Only images and PDFs are allowed.";
      return false;
    }

    var fileSize = imageUploadInput.files[0].size; // in bytes

    // Convert fileSize to MB
    var fileSizeInMB = fileSize / (1024 * 1024);

    // Check if the file size is within the specified limit
    if (fileSizeInMB > maxSizeMB) {
      // imageUploadInput.value = ''; // Clear the selected file
      imageUploadError.textContent = `File size should not be greater than ${maxSizeMB} MB`;
      return false;
    }

    imageUploadError.textContent = ""; // Clear any previous error messages
    return true;
  } else {
    return true;
  }
}

function validateRating() {
  var ratingField = document.getElementById("rating");
  var rating = parseFloat(ratingField.value);
  var errorElement = document.getElementById("ratingError");

  // Clear any existing error message
  errorElement.textContent = "";

  // Check if rating is a valid number
  if (isNaN(rating)) {
    errorElement.textContent = "Rating must be a valid number.";
    return;
  }
  errorElement.textContent = "";
}

var currentUrl = window.location.href;
var baseUrl = currentUrl.split("/").slice(0, 3).join("/");

function populateStates(country) {
  var countryId = country;
  console.log(countryId);
  // document.getElementById('state-display').textContent = 'Select State';
  var stateDropdown = document
    .getElementById("state-menu")
    .querySelector(".dropdown-options");
  stateDropdown.innerHTML = '<div class="dropdown-item">Loading...</div>';
  var apiUrl = baseUrl + "/api/v1/guest/states/?country_id=" + countryId;
  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      stateDropdown.innerHTML = ""; // Clear loading option
      data.responseData.forEach((state) => {
        var option = document.createElement("div");
        option.classList.add("dropdown-item");
        option.textContent = state.name;
        option.onclick = function () {
          selectOption("state", "state-display", state.id, state.name);
          populateCities(state.id);
          closeDropdown("city-menu");

          document.getElementById("city").value = "";
        };
        stateDropdown.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching states:", error));
}
function populateCities(state) {
  var stateId = state;
  var cityDisplay = document.getElementById("city-display");
  var cityDropdown = document
    .getElementById("city-menu")
    .querySelector(".dropdown-options");
  cityDisplay.textContent = "Select City"; // Clear city display
  cityDropdown.innerHTML = '<div class="dropdown-item">Loading...</div>';
  var apiUrl = baseUrl + "/api/v1/guest/cities/?state_id=" + stateId;
  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      cityDropdown.innerHTML = ""; // Clear loading option
      data.responseData.forEach((city) => {
        var option = document.createElement("div");
        option.classList.add("dropdown-item");
        option.textContent = city.name;
        option.onclick = function () {
          selectOption("city", "city-display", city.id, city.name);
        };
        cityDropdown.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching cities:", error));
}

function UpdatedpopulateCities(state) {
  var stateId = state;
  var cityDropdown = document
    .getElementById("city-menu")
    .querySelector(".dropdown-options");
  cityDropdown.innerHTML = '<div class="dropdown-item">Loading...</div>';
  var apiUrl = baseUrl + "/api/v1/guest/cities/?state_id=" + stateId;
  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      cityDropdown.innerHTML = ""; // Clear loading option
      data.responseData.forEach((city) => {
        var option = document.createElement("div");
        option.classList.add("dropdown-item");
        option.textContent = city.name;
        option.onclick = function () {
          selectOption("city", "city-display", city.id, city.name);
        };
        cityDropdown.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching cities:", error));
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie name matches the desired format
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function validateProfileImageSize(inputId, errorId, maxSizeMB) {
  var imageUploadInput = document.getElementById(inputId);
  var imageUploadError = document.getElementById(errorId);

  if (imageUploadInput.files.length > 0) {
    // Define the valid file types, excluding PDF
    var validImageTypes = [
      "image/jpeg",
      "image/png",
      "image/jpg",
      "image/bmp",
      "image/webp",
      "image/svg+xml",
    ];
    var fileType = imageUploadInput.files[0].type;

    if (!validImageTypes.includes(fileType)) {
      imageUploadInput.value = ""; // Clear the selected file
      imageUploadError.textContent = "Only images are allowed.";
      return;
    }

    var fileSize = imageUploadInput.files[0].size; // in bytes

    // Convert fileSize to MB
    var fileSizeInMB = fileSize / (1024 * 1024);

    // Check if the file size is within the specified limit
    if (fileSizeInMB > maxSizeMB) {
      imageUploadInput.value = ""; // Clear the selected file
      imageUploadError.textContent = `File size should not be greater than ${maxSizeMB} MB`;
      return;
    }

    imageUploadError.textContent = ""; // Clear any previous error messages
  }
}

function updateFileName(inputId) {
  // Get the input file element and its selected file
  const inputFile = document.getElementById(inputId);
  const file = inputFile.files[0];

  // Get the span element where the file name should be displayed
  const fileNameSpanId = `file-upload-name-${inputId}`;
  const fileNameSpan = document.getElementById(fileNameSpanId);

  // Check if a file is selected
  if (file) {
    let fileName = file.name;

    // Truncate file name to 10 characters and add ellipsis if needed
    if (fileName.length > 10) {
      fileName = fileName.slice(0, 13) + "...";
    }

    // Set the truncated file name to the span element
    fileNameSpan.innerText = fileName;
  } else {
    // If no file is selected, reset the span element's text
    fileNameSpan.innerText = "Choose File";
  }
}

document.body.addEventListener("click", function (event) {
  // Check if the clicked element is not inside any of the dropdowns
  var genderDropdown =
    event.target.closest(".dropdown") && !event.target.closest("#gender-menu");
  var countryDropdown =
    event.target.closest(".dropdown") && !event.target.closest("#country-menu");
  var stateDropdown =
    event.target.closest(".dropdown") && !event.target.closest("#state-menu");
  var cityDropdown =
    event.target.closest(".dropdown") && !event.target.closest("#city-menu");

  function closeDropdown(dropdownId) {
    var dropdownMenu = document.getElementById(dropdownId);
    if (dropdownMenu) {
      dropdownMenu.style.display = "none";
    }
  }
  // If clicked outside of any dropdown, close all dropdowns
  if (!genderDropdown && !countryDropdown && !stateDropdown && !cityDropdown) {
    closeDropdown("gender-menu");
    closeDropdown("country-menu");
    closeDropdown("state-menu");
    closeDropdown("city-menu");
  }
});
