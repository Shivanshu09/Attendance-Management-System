
function createTable(data)
{   
    students = data.students;
    table = document.getElementById('tableBody')
    // var button = '<td><label>Present</label><input type="radio" name="set_status" value="Present" checked><label>Absent </label><input type="radio" name="set_status" value="Absent"></td>'
    var button = '<td name = "chck"><input  type="checkbox"></td>' 

    table.innerHTML = "";
    for(var i = 0;i<students.length;i++)
    {   
        var trow = document.createElement('tr')
        var tid = document.createElement('td')
        tid.innerText = students[i].id
        tid.setAttribute("name","id")
        var tname = document.createElement('td')
        tname.setAttribute("name","st_name")
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

function getAttendanceData()
{
    var sem = parseInt($('#input1').val());
    var sec = $('#input2').val();
    trows = document.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    var students = [];
    var attend = {};
    for(var i = 0;i<trows.length;i++)
    {
        var tds = trows[i].getElementsByTagName("td");
        var user = {};
        for(var j = 0;j<tds.length;j++)
        {
            
            if (tds[j].getAttribute("name").localeCompare("id") == 0)
            {
                user['id'] = tds[j].innerText;
            }
        }

        var checkbox = trows[i].getElementsByTagName("input")[0];
        if (checkbox.checked)
        {
            user['present'] = true;
        }
        else
            user['present'] = false;

        
        students.push(user);
    }
    attend['students'] = students;
    attend['date'] = $('#date-picker').val()
    attend['semester'] = sem
    attend['section'] = sec
    return attend;
}

function postAttendanceData()
{
    data = getAttendanceData()
    console.log("POST")
    $.ajax({
        url: '/markattendance',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function(){
            alert("Succesfully Saved")
        },
        data: JSON.stringify(data)
    });
}

$(document).ready(function() {
    $('#submitButton')[0].addEventListener("click",getClassData);
    $('#save')[0].addEventListener("click",postAttendanceData);
});