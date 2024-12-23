let selectedClassId = null;

// Chọn lớp
function handleClassSelection(selectElement) {
    selectedClassId = selectElement.value;  // Lấy giá trị lớp đã chọn
}

// Thêm học sinh vào lớp
function handleAddToClass(studentId) {
    if (!selectedClassId) {
        alert("Vui lòng chọn lớp trước khi thêm học sinh!");
        return;
    }
    // Gửi dữ liệu đến server để thêm học sinh vào lớp
    fetch('/api/add_hoc', {
        method: 'POST',
        body: JSON.stringify({
            key: "creat_hoc",
            data: [{
                "student_id": studentId,
                "class_id": selectedClassId
            }]
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            alert("Phản hồi từ server: " + JSON.stringify(data));
            console.log("Dữ liệu trả về từ server:", data);
            if (data.message === 'add_hoc added successfully') {
                // Xóa học sinh khỏi bảng "Chưa Có Lớp"
                const studentRow = document.querySelector(`button[onclick="handleAddToClass('${studentId}')"]`).closest('tr');
                const cells = Array.from(studentRow.children).slice(0, -1); // Lấy tất cả các ô trừ cột hành động
                studentRow.remove();

                // Thêm học sinh vào bảng "Danh Sách Học Sinh Trong Lớp"
                const studentsInClassTable = document.querySelector('.students-in-class');
                const newRow = document.createElement('tr');

                // Tạo các ô từ dữ liệu của học sinh
                cells.forEach(cell => {
                    const newCell = document.createElement('td');
                    newCell.className = 'border px-4 py-2';
                    newCell.textContent = cell.textContent;
                    newRow.appendChild(newCell);
                });

                // Thêm cột "Lớp"
                const classCell = document.createElement('td');
                classCell.className = 'border px-4 py-2';
                classCell.textContent = document.querySelector('.class-select option:checked').textContent;
                newRow.appendChild(classCell);

                studentsInClassTable.appendChild(newRow);

                alert("Thêm học sinh vào lớp thành công!");
            } else {
                alert("Check---> " + JSON.stringify(data));
                //alert("Có lỗi xảy ra: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Không thể thêm học sinh vào lớp. Vui lòng thử lại!");
        });
}

function StudentNoClass() {
    fetch('/api/get_student_no_class')
        .then(response => response.json())
        .then(data => {
            const studentsTableBody = document.querySelector('.students-no-class');
            studentsTableBody.innerHTML = ''; // Clear current rows
            data.students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="border px-4 py-2">${student.ma_hoc_sinh}</td>
                    <td class="border px-4 py-2">${student.ho_ten}</td>
                    <td class="border px-4 py-2">${student.gioi_tinh}</td>
                    <td class="border px-4 py-2">${student.ngay_sinh}</td>
                    <td class="border px-4 py-2">${student.dia_chi}</td>
                    <td class="border px-4 py-2">
                        <button class="bg-blue-500 text-white px-2 py-1 rounded"
                                data-id="${student.ma_hoc_sinh}" onclick="handleAddToClass(this)">
                            Thêm
                        </button>
                    </td>
                `;
                studentsTableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching students:', error));
}
function GetClass(classId) {
    fetch('/api/get_class', {
        method: 'POST',
        body: JSON.stringify({
            "class_id": classId
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(res => res.json())  // Lưu ý phải gọi .json() ở đây
        .then(data => {
            console.log(data);
            // Xử lý dữ liệu trả về từ API
        })
        .catch(error => {
            console.error('Error fetching class:', error);
        });
}


function handleSearchStudent() {
    const classInput = document.querySelector('.class-input').value.trim();
    const studentNameInput = document.querySelector('.student-name-input').value.trim();
    const academicYear = document.querySelector('.academic-year-select').value;

    if (!academicYear || !classInput) {
        alert("Vui lòng chọn năm học và nhập lớp!");
        return;
    }

    // Gửi yêu cầu đến server
    fetch('/api/get_student_scores', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            class: classInput,
            name: studentNameInput,
            year: academicYear,
        }),
    })
        .then(response => response.json())
        .then(data => {
            console.log("Kết quả:", data);

            if (data.success) {
                const tableBody = document.querySelector('.score-table-body');
                tableBody.innerHTML = ''; // Xóa các hàng cũ

                // Thêm từng dòng điểm vào bảng
                data.scores.forEach((student, index) => {
                    const row = `
                        <tr>
                            <td class="border px-4 py-2">${index + 1}</td>
                            <td class="border px-4 py-2">${student.name}</td>
                            <td class="border px-4 py-2">${student.class}</td>
                            <td class="border px-4 py-2">${student.averageHK1}</td>
                            <td class="border px-4 py-2">${student.averageHK2}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            } else {
                alert("Không tìm thấy dữ liệu phù hợp.");
            }
        })
        .catch(error => {
            console.error('Lỗi:', error);
            alert("Không thể lấy dữ liệu học sinh. Vui lòng thử lại!");
        });
}
