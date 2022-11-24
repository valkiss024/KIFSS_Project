jQuery(document).ready(function(){
    $('#exportbutton').click(function(){
        html2canvas(document.querySelector('#devices')).then((canvas) => {
            let base64image = canvas.toDataURL('image/png');
           // console.log(base64image);

            let pdf = new jsPDF('p', 'px', [1920, 1440]);
            pdf.addImage(base64image, 'PNG', 15, 15, 1920, 1220);
            pdf.save('webtylepress-throw.pdf');
        });
    });
});
