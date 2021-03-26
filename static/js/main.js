const selectElement = (e)=> document.querySelector(e);
const selectElements = (e)=> document.querySelectorAll(e);







// validating link
function validateLink(link) {
    var re = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/;
    return re.test(String(link));
}


const input_overlay = selectElement('.search-input');
const link_input = selectElement('#link-input');
selectElement('#search-btn').addEventListener('click',(e)=>{
    e.preventDefault();
    if(validateLink(link_input.value)){
        selectElement('.search-box p').style.display="none"
        selectElement('.loading').style.display="block";
        $.get("/get", {link: 'https://en.wikipedia.org/wiki/Alaouite_dynasty' }).done(function(data) {
        selectElement('.tree').innerHTML= '<h1 id="familyname"></h1>' + data;

        let title = selectElement('.familytree').getAttribute('data-name');
        selectElement('#familyname').innerHTML = `Family Tree : ${title}`;
        selectElement('.loading').style.display="block";
        setTimeout(()=>{
            input_overlay.classList.add('slide');
        },1000);
        });
    }else{
        selectElement('.search-box p').style.display="block"
    }
});
