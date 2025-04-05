var clearButton = document.getElementById('clear-button');
clearButton.disabled = true;

var searchValue = document.getElementById('search-bar').value;
var fromDateValue = document.getElementById('end-date-selector').value;
var toDateValue = document.getElementById('start-date-selector').value;
var statusValue = document.getElementById('status-select').value;

var clearButton = document.getElementById('clear-button');

if (searchValue.trim() !== '' || fromDateValue.trim() !== '' || toDateValue.trim() !== '' || statusValue !== ('All' || 'ALL' || '' )) {
    clearButton.disabled = false; // Enable the clear button
} else {
    clearButton.disabled = true; // Disable the clear button

}



