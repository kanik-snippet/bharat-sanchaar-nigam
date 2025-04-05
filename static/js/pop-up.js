//All pop-up javascript code 



//////////////////////////////////////////// BLock-Unblock , Accept-Reject ,Delete Pop-Up ////////////////////////////////////////////

function showStatusBlockPopup(statusUrl) {

    document.getElementById("statusblockOverlay").style.display = "block";
    document.getElementById("statusblockpopupCard").style.display = "block";
    document.getElementById("statusblockForm").action = statusUrl;
}

function hideStatusBlockPopup() {
    document.getElementById("statusblockOverlay").style.display = "none";
    document.getElementById("statusblockpopupCard").style.display = "none";
}

function confirmStatusBlock() {

    document.getElementById('blockLoader').style.display = 'inline-block';
    document.getElementById("block-button").disabled = true;
    document.getElementById("block-cancel").disabled = true;
    var form_ =document.getElementById("statusblockForm");
    var statusUrl=form_.action;
          // Get the query parameters from the current URL
          var params = window.location.href.split('?')[1];
          // Check if the statusUrl already contains a query string
          var delimiter = statusUrl.includes('?') ? '&' : '?';
          // Concatenate the statusUrl and the query parameters
          var url = statusUrl + delimiter + params;
      
          // Redirect to the constructed URL
          window.location.href = url;
    
}


function showStatusUnblockPopup(statusUrl) {
    document.getElementById("statusunblockOverlay").style.display = "block";
    document.getElementById("statusunblockpopupCard").style.display = "block";
    document.getElementById("statusunblockForm").action = statusUrl;
}

function hideStatusUnblockPopup() {
    document.getElementById("statusunblockOverlay").style.display = "none";
    document.getElementById("statusunblockpopupCard").style.display = "none";
}

function confirmStatusUnblock() {
    document.getElementById('unblockLoader').style.display = 'inline-block';
    document.getElementById("unblock-button").disabled = true;
    document.getElementById("unblock-cancel").disabled = true;
    // document.getElementById("statusunblockForm").submit();
    var form_ =document.getElementById("statusunblockForm");
    var statusUrl=form_.action;
          // Get the query parameters from the current URL
          var params = window.location.href.split('?')[1];
          // Check if the statusUrl already contains a query string
          var delimiter = statusUrl.includes('?') ? '&' : '?';
          // Concatenate the statusUrl and the query parameters
          var url = statusUrl + delimiter + params;
      
          // Redirect to the constructed URL
          window.location.href = url;
    
  }
// function confirmStatusChange(statusUrl) {
//     document.getElementById("statusOverlay").style.display = "block";
//     document.getElementById("statusPopupCard").style.display = "block";
//     document.getElementById("statusForm").action = statusUrl;
// }

// function confirmStatusChange() {
//     document.getElementById("statusOverlay").style.display = "none";
//     document.getElementById("statusPopupCard").style.display = "none";
// }

// function confirmStatusChange() {
//     document.getElementById('loader').style.display = 'inline-block';
//     document.getElementById("confirm-button").disabled = true;
//     document.getElementById("cancel-button").disabled = true;
//     // document.getElementById("statusunblockForm").submit();
//     var form_ =document.getElementById("statusForm");
//     var statusUrl=form_.action;
//           // Get the query parameters from the current URL
//           var params = window.location.href.split('?')[1];
//           // Check if the statusUrl already contains a query string
//           var delimiter = statusUrl.includes('?') ? '&' : '?';
//           // Concatenate the statusUrl and the query parameters
//           var url = statusUrl + delimiter + params;
      
//           // Redirect to the constructed URL
//           window.location.href = url;
    
//   }


  function showDeleteUserPopup(statusUrl) {
    document.getElementById("deleteuserOverlay").style.display = "block";
    document.getElementById("deleteuserpopupCard").style.display = "block";
    document.getElementById("deleteuserForm").action = statusUrl;
}

function hideDeleteUserPopup() {
    document.getElementById("deleteuserOverlay").style.display = "none";
    document.getElementById("deleteuserpopupCard").style.display = "none";
}

function confirmStatusUnblock() {
    document.getElementById('deleteLoader').style.display = 'inline-block';
    document.getElementById("delete-button").disabled = true;
    document.getElementById("delete-cancel").disabled = true;
    var form_ =document.getElementById("deleteuserForm");
    var statusUrl=form_.action;
          // Get the query parameters from the current URL
          var params = window.location.href.split('?')[1];
          // Check if the statusUrl already contains a query string
          var delimiter = statusUrl.includes('?') ? '&' : '?';
          // Concatenate the statusUrl and the query parameters
          var url = statusUrl + delimiter + params;
      
          // Redirect to the constructed URL
          window.location.href = url;
    
  }
  
  ////////////////////////////////////////Accept -Reject/////////////////////////////////////
  function showAcceptPopup(statusUrl) {
    document.getElementById("acceptOverlay").style.display = "block";
    document.getElementById("acceptpopupCard").style.display = "block";
    document.getElementById("acceptForm").action = statusUrl;
  }
  
  function hideAcceptPopup() {
    document.getElementById("acceptOverlay").style.display = "none";
    document.getElementById("acceptpopupCard").style.display = "none";
  }
  
  function confirmAccept() {
    document.getElementById('acceptLoader').style.display = 'inline-block';
    document.getElementById("popup-accept-button").disabled = true;
    document.getElementById("popup-approve-cancel").disabled = true;
    document.getElementById("acceptForm").submit();
}



function showRejectPopup(statusUrl) {
  document.getElementById("rejectOverlay").style.display = "block";
  document.getElementById("rejectpopupCard").style.display = "block";
  document.getElementById("rejectForm").action = statusUrl;
}

function hideRejectPopup() {
  document.getElementById("rejectOverlay").style.display = "none";
  document.getElementById("rejectpopupCard").style.display = "none";
}

function confirmReject() {
  var rejectReason = document.getElementById('reject_reason').value;
    if (rejectReason.trim() === '') {
        // If reject reason is not filled, prevent submission
        document.getElementById('reject_reason_error').innerText = "Reason is required.";
        return false; // Prevent form submission
    } else {
        // If reject reason is filled, submit the form
        document.getElementById('rejectLoader').style.display = 'inline-block';
        document.getElementById("popup-reject-button").disabled = true;
        document.getElementById("popup-reject-cancel").disabled = true;
        document.getElementById("rejectForm").submit();
    }
}

function validateResponse(){
  var replyMessage = document.getElementById('reject_reason').value.trim();
  var replyMessageError = document.getElementById('reject_reason_error');
  replyMessageError.innerText = '';
  }

//Doctor Management Category Delete 

function showDeletePopup(deleteUrl) {

    document.getElementById("deleteOverlay").style.display = "block";
    document.getElementById("popupCard").style.display = "block";
    document.getElementById("deleteForm").action = deleteUrl;
  }

  function hideDeletePopup() {
    document.getElementById("deleteOverlay").style.display = "none";
    document.getElementById("popupCard").style.display = "none";
  }

  function confirmDelete() {
    document.getElementById('deleteLoader').style.display = 'inline-block';
    document.getElementById("del_button_pop_up").disabled = true;
    document.getElementById("del-cancel-pop-up").disabled = true;
    document.getElementById("deleteForm").submit();
  }


  //new policy reject (used when no reasons provided )
  function newpolicystatusreject() {

    var rejectReason = document.getElementById('reject_reason').value;
    if (rejectReason.trim() === '') {
        // If reject reason is not filled, prevent submission
        document.getElementById('reject_reason_error').innerText = "Reason is required.";
        return false; // Prevent form submission
    } else {
        // If reject reason is filled, submit the form

        document.getElementById('unblockLoader').style.display = 'inline-block';
        document.getElementById("unblock-button").disabled = true;
        document.getElementById("unblock-cancel").disabled = true;
        document.getElementById("statusunblockForm").submit();
    }
} 
function validateTextarea() {
    var textarea = document.getElementById('reject_reason');
    var errorMessage = document.getElementById('reject_reason_error');
    errorMessage.textContent = '';
       
    
}

///////////////////////////////////////subadmin/////////////////////
 function subadminDeletePopup(subadminId) {
    // Set the subadmin id in the hidden input field
    document.getElementById('subadmin_id').value = subadminId;
    // Show the overlay and popup
    document.getElementById('deleteOverlay').style.display = 'block';
    document.getElementById('popupCard').style.display = 'block';
  }



////////////////////////////////////////////////////////////////// Order status POP-UP////////////////////////////////////////////
function showStatusChangePopup(statusUrl,status) {
  var statusText = "";
  var confirmationText = "";
  if (status == 'Placed') {
    statusText = "Mark as Confirmed";
    confirmationText = "Are you sure you want to mark as confirmed?";
} else if (status == 'Confirmed') {
    statusText = "Mark as Dispatched";
    confirmationText = "Are you sure you want to mark as dispatched?";
} else if (status == 'Dispatched') {
    statusText = "Mark as Delivered";
    confirmationText = "Are you sure you want to mark as delivered?";
}
  document.getElementById("statusTitle").innerHTML = statusText;
  document.getElementById("statusConfirmation").innerHTML = confirmationText;
  document.getElementById("statusblockOverlay").style.display = "block";
  document.getElementById("statusblockpopupCard").style.display = "block";
  document.getElementById("statusblockForm").action = statusUrl;
}


