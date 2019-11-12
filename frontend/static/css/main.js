
function createTable(data)
{   
    students = data.students;
    table = document.getElementById('tableBody')
    var button = '<td><label>Present</label><input type="radio" name="set_status" value="Present" checked><label>Absent </label><input type="radio" name="set_status" value="Absent"></td>'
 
    table.innerHTML = "";
    for(var i = 0;i<students.length;i++)
    {   
        var trow = document.createElement('tr')
        var tid = document.createElement('td')
        tid.innerText = students[i].id
        var tname = document.createElement('td')
        tname.innerText = students[i].name
        trow.append(tid)
        trow.append(tname)
        trow.innerHTML += button
        table.append(trow)
    }
}

function getClassData()
{
    var sem = parseInt($('#input1').val());
    var sec = $('#input2').val();

    var classroom = {
                semester: sem,
                section: sec
               };
    $.ajax({
        url: '/getStudents',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: createTable,
        data: JSON.stringify(classroom)
    });
}

$(document).ready(function() {
    $('#submitButton')[0].addEventListener("click",getClassData);
});