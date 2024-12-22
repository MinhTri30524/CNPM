document.addEventListener("DOMContentLoaded", () => {
    let selectedClassId = null;
    const handleClassSelection = (event) => {
        selectedClassId = event.target.value;
    };
    const handleAddToClass = (event) => {
        if (!selectedClassId) {
            alert("Vui lòng chọn lớp trước khi thêm học sinh!");
            return;
        }

        // Lấy thông tin học sinh từ dòng hiện tại
        const button = event.target;
        const studentRow = button.closest("tr");    
        const studentData = Array.from(studentRow.children).slice(0, -1).map(td => td.textContent);

        // Tìm bảng danh sách học sinh trong lớp
        const studentsInClassTable = document.querySelector(".students-in-class");

        // Tạo dòng mới
        const newRow = document.createElement("tr");
        studentData.forEach(data => {
            const cell = document.createElement("td");
            cell.className = "border px-4 py-2";
            cell.textContent = data;
            newRow.appendChild(cell);
        });

        // Thêm cột "Lớp"
        const classCell = document.createElement("td");
        classCell.className = "border px-4 py-2";
        const className = document.querySelector(".class-select option:checked").textContent;
        classCell.textContent = className;
        newRow.appendChild(classCell);

        studentsInClassTable.appendChild(newRow);

        // Xóa học sinh khỏi danh sách "Chưa Có Lớp"
        studentRow.remove();
    };

    // Gán sự kiện cho select lớp
    document.querySelector(".class-select").addEventListener("change", handleClassSelection);

    // Gán sự kiện cho các nút "Thêm" học sinh
    document.querySelectorAll(".add-to-class-btn").forEach(button => {
        button.addEventListener("click", handleAddToClass);
    });

    function loadStudentsInClass(classId) {
        if (classId) {
            fetch(`/students_in_class/${classId}`)
                .then(response => response.json())
                .then(data => {
                    const studentsTableBody = document.querySelector('.student-table-body');
                    studentsTableBody.innerHTML = ''; // Clear current rows
                    data.students.forEach((student, index) => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td class="border px-4 py-2">${index + 1}</td>
                            <td class="border px-4 py-2">${student.name}</td>
                            <td class="border px-4 py-2">
                                <input type="number" class="score-15p" data-student-id="${student.id}" />
                            </td>
                            <td class="border px-4 py-2">
                                <input type="number" class="score-45p" data-student-id="${student.id}" />
                            </td>
                            <td class="border px-4 py-2">
                                <input type="number" class="final-score" data-student-id="${student.id}" />
                            </td>
                        `;
                        studentsTableBody.appendChild(row);
                    });
                });
        } else {
            document.querySelector('.student-table-body').innerHTML = ''; // Clear table if no class selected
        }
    }

    // Hàm cập nhật số cột điểm 15 phút
    function updateScoreColumns(scoreType, colCount) {
        const scoreInputs = document.querySelectorAll(`.${scoreType}`);
        scoreInputs.forEach(input => {
            input.setAttribute('max', colCount); // Set max value of columns
        });
    }

    // Hàm lưu điểm của học sinh
    function saveScores() {
        const scores = [];
        document.querySelectorAll('.student-table-body tr').forEach(row => {
            const studentId = row.querySelector('.score-15p').getAttribute('data-student-id');
            const score15p = row.querySelector('.score-15p').value;
            const score45p = row.querySelector('.score-45p').value;
            const finalScore = row.querySelector('.final-score').value;

            scores.push({ studentId, score15p, score45p, finalScore });
        });

        fetch('/save_scores', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scores })
        })
            .then(response => response.json())
            .then(data => {
                alert('Điểm đã được lưu!');
            });
    }

    // Sự kiện khi chọn lớp
    document.querySelector('.class-select').addEventListener('change', function () {
        const classId = this.value;
        loadStudentsInClass(classId);
    });

    // Sự kiện khi nhập số cột điểm 15 phút
    document.querySelector('.col-15p-input').addEventListener('input', function () {
        const colCount = this.value;
        updateScoreColumns('score-15p', colCount);
    });

    // Sự kiện khi nhập số cột điểm 1 tiết
    document.querySelector('.col-45p-input').addEventListener('input', function () {
        const colCount = this.value;
        updateScoreColumns('score-45p', colCount);
    });

    // Sự kiện khi nhấn nút lưu điểm
    document.querySelector('.save-button').addEventListener('click', function () {
        saveScores();
    });
});


// Hàm lấy dữ liệu điểm học sinh từ API
function fetchStudentsData() {
    fetch('/api/students')
        .then(response => response.json())
        .then(data => {
            // Gọi hàm hiển thị bảng điểm với dữ liệu lấy được từ API
            displayScoreTable(data);
        })
        .catch(error => {
            console.error('Error fetching students data:', error);
        });
}

// Hàm hiển thị bảng điểm
function displayScoreTable(students) {
    const tableBody = document.querySelector('.score-table-body');
    tableBody.innerHTML = '';  // Clear table before adding new rows

    students.forEach((student, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="border px-4 py-2">${index + 1}</td>
            <td class="border px-4 py-2">${student.name}</td>
            <td class="border px-4 py-2">${student.class}</td>
            <td class="border px-4 py-2">${student.scoreHK1}</td>
            <td class="border px-4 py-2">${student.scoreHK2}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Hàm xử lý sự kiện xuất điểm
function handleExport() {
    const academicYear = document.querySelector('.academic-year-select').value;
    const studentName = document.querySelector('.student-name-input').value;
    const classInput = document.querySelector('.class-input').value;

    // Lọc dữ liệu giả lập theo thông tin người dùng nhập
    fetch('/api/students_point')
        .then(response => response.json())
        .then(studentsData => {
            const filteredStudents = studentsData.filter(student => {
                return (
                    (academicYear ? student.academicYear === academicYear : true) &&
                    (studentName ? student.name.includes(studentName) : true) &&
                    (classInput ? student.class.includes(classInput) : true)
                );
            });

            // Hiển thị bảng điểm sau khi lọc
            displayScoreTable(filteredStudents);
        });
}

// Gắn sự kiện cho nút xuất
document.querySelector('.export-btn').addEventListener('click', handleExport);

// Lấy dữ liệu học sinh khi trang được load
window.onload = fetchStudentsData;


function handleGenerateListClick(buttonElement) {
    // Tìm phần tử tbody chứa danh sách học sinh
    const studentsTableBody = buttonElement.closest("div").querySelector(".students-in-class");
    const studentCount = studentsTableBody.children.length;

    // Tìm thẻ hiển thị thông báo trong cùng container
    const errorMessage = buttonElement.closest("div").querySelector("p");

    // Kiểm tra số lượng học sinh
    if (studentCount <= 40) {
        errorMessage.textContent = "Danh sách lớp đã được lập thành công!";
        errorMessage.classList.remove("hidden");
        errorMessage.classList.replace("text-red-500", "text-green-500");
    } else {
        errorMessage.textContent = "Quá số lượng học sinh trong lớp!";
        errorMessage.classList.remove("hidden");
        errorMessage.classList.replace("text-green-500", "text-red-500");
    }
}
