const selectElement = document.getElementById('divs');
const formElement = document.getElementById('myForm');

selectElement.addEventListener('change', () => {
    formElement.submit();
});