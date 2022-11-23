jQuery(document).ready(function(){
    $('#exportbutton').click(function(){
        html2canvas(document.querySelector('#devices')).then((canvas) => {
            let base64image = canvas.toDataURL('image/png');
           // console.log(base64image);

            let pdf = new jsPDF('p', 'px', [1600, 1080]);
            pdf.addImage(base64image, 'PNG', 15, 15, 1812, 1130);
            pdf.save('webtylepress-throw.pdf');
        });
    });
});











// const printBtn = document.getElementById('exportbutton');

// printBtn.addEventListener('click', function() {
//     print();
// });

// let htmlPDF = document.getElementById("devices");
// let exportPDF = document.getElementById("exportbutton");
// exportPDF.onclick = (e) => html2pdf(htmlPDF);
// exportPDF.onclick = (e) => html2pdf(base64image)