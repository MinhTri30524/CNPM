let selectedClassId = null;

// Chọn lớp
function handleClassSelection(selectElement) {
    selectedClassId = selectElement.value; // Lấy class_id từ chọn lớp

    // Kiểm tra nếu có lớp được chọn
    if (!selectedClassId) {
        alert("Vui lòng chọn lớp!");
        return;
    }

    // Tạo dữ liệu request
    const requestData = {
        data: [{
            class_id: selectedClassId
        }]
    };

    // Gửi request để lấy danh sách học sinh
    fetch('/api/get_students_by_class', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData) // Gửi dữ liệu lớp
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to add to hoc: " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.message === 'Students fetched successfully') {
                // Hiển thị danh sách học sinh trong lớp
                const studentsInClassTable = document.querySelector('.students-in-class');
                studentsInClassTable.innerHTML = '';  // Xóa nội dung cũ

                data.data.forEach((student, index) => {
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
                    <td class="border px-4 py-2">${index + 1}</td>
                    <td class="border px-4 py-2">${student.ho_ten}</td>
                    <td class="border px-4 py-2">${student.gioi_tinh}</td>
                    <td class="border px-4 py-2">${student.ngay_sinh}</td>
                    <td class="border px-4 py-2">${student.dia_chi}</td>
                    <td class="border px-4 py-2">${student.lop_hoc_id}</td>
                `;
                    studentsInClassTable.appendChild(newRow);
                });
            } else {
                alert("Không thể tải danh sách học sinh.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Đã xảy ra lỗi khi tải dữ liệu.");
        });
}



function handleAddToClass(studentId) {
    if (!selectedClassId) {
        alert("Vui lòng chọn lớp trước khi thêm học sinh!");
        return;
    }

    // Payload cho API update_student_class
    const updateStudentRequest = {
        data: [{
            "ma_hoc_sinh": studentId,
            "lop_hoc_id": selectedClassId
        }]
    };

    // Gửi yêu cầu để cập nhật bảng student
    fetch('/api/update_student_class', {
        method: 'POST',
        body: JSON.stringify(updateStudentRequest),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to update student class: " + response.statusText);
            }
            return response.json();
        })
        .then(updateData => {
            if (updateData.message === 'Students updated successfully') {
                // Cập nhật giao diện sau khi thành công
                const studentRow = document.querySelector(`button[onclick="handleAddToClass('${studentId}')"]`).closest('tr');
                const cells = Array.from(studentRow.children).slice(0, -1); // Lấy tất cả các ô trừ cột hành động
                studentRow.remove();

                const studentsInClassTable = document.querySelector('.students-in-class');
                const newRow = document.createElement('tr');

                cells.forEach(cell => {
                    const newCell = document.createElement('td');
                    newCell.className = 'border px-4 py-2';
                    newCell.textContent = cell.textContent;
                    newRow.appendChild(newCell);
                });

                const classCell = document.createElement('td');
                classCell.className = 'border px-4 py-2';
                classCell.textContent = document.querySelector('.class-select option:checked').textContent;
                newRow.appendChild(classCell);

                studentsInClassTable.appendChild(newRow);

                alert("Cập nhật học sinh vào lớp thành công!");
            } else {
                throw new Error("Lỗi khi cập nhật bảng student: " + JSON.stringify(updateData));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Không thể cập nhật thông tin học sinh. Vui lòng thử lại!");
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
