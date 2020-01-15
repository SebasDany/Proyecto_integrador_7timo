const btnDelete= document.querySelectorAll('.btn-delete');
const btnInsert= document.querySelectorAll('.btn-block');

if(btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('Are you sure you want to delete it?')){
        e.preventDefault();
      }
    });
  })
}
if(btnInsert) {
  const btnArray1 = Array.from(btnInsert);
  btnArray1.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('Insertando datos , Esta seguro? ')){
        e.preventDefault();
      }
    });
  })
}


