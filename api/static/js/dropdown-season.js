const selectElement = document.getElementById('seasons');
const formElement = document.getElementById('myForm');

selectElement.addEventListener('change', () => {
    formElement.submit();
});