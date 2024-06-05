document.addEventListener('DOMContentLoaded', () => {
    const timeGrid = document.querySelector('.time-grid'); // 시간 슬롯을 표시할 그리드
    const modal = document.getElementById('modal'); // 모달 창
    const closeModal = document.querySelector('.close'); // 모달 닫기 버튼
    const datePicker = document.getElementById('date-picker'); // 날짜 선택기
    const weekTitle = document.getElementById('week-title'); // 주 제목
    const todoList = document.querySelector('.todo-list ul'); // 할 일 목록

    let currentWeekStart = new Date(2024, 3, 14); // 현재 주의 시작일 (2024년 4월 14일)
    let currentWeekEnd = new Date(currentWeekStart); // 현재 주의 끝일
    currentWeekEnd.setDate(currentWeekEnd.getDate() + 6); // 주의 끝일을 계산
    let isDragging = false; // 드래그 상태 여부
    let startSlot = null; // 드래그 시작 슬롯
    let endSlot = null; // 드래그 끝 슬롯
    let lastSelectedSlot = null; // 마지막으로 선택된 슬롯
    let selectedSlotsIndices = []; // 선택된 슬롯의 인덱스를 저장하기 위한 배열
    let colorIndex = 0; // 색상을 선택하기 위한 인덱스

    // 색상 배열
    const colors = ['#fec5bb', '#fcd5ce', '#fae1dd', '#f8edeb', '#e8e8e4', '#d8e2dc', '#ece4db', '#ffe5d9', '#ffd7ba'];

    // 초기화
    todoList.innerHTML = '';
   
    // 날짜 선택 전 "Time To Do" 표시
    weekTitle.textContent = "Time To Do";

    // 시간 슬롯을 생성
    for (let i = 0; i < 24 * 6; i++) { // 하루에 24 슬롯, 주당 6일
        const timeSlot = document.createElement('div');
        timeSlot.classList.add('time-slot');
        timeSlot.dataset.index = i;
        timeSlot.addEventListener('mousedown', handleMouseDown); // 마우스 다운 이벤트 핸들러
        timeSlot.addEventListener('mouseover', handleMouseOver); // 마우스 오버 이벤트 핸들러
        timeSlot.addEventListener('mouseup', handleMouseUp); // 마우스 업 이벤트 핸들러
        timeSlot.addEventListener('contextmenu', handleContextMenu); // 마우스 우클릭 이벤트 핸들러
        timeGrid.appendChild(timeSlot); // 시간 슬롯을 그리드에 추가
    }

    // 인덱스를 시간 문자열로 변환하는 함수
    function convertIndexToTime(index) {
        const hours = Math.floor(index / 6) + 6; // 시간 인덱스를 6시부터 시작하도록 조정
        const minutes = (index % 6) * 10;
        const adjustedHours = hours >= 24 ? hours - 24 : hours;
        const period = hours >= 24 ? 'AM' : 'PM';
        return `${adjustedHours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    }

    // 모달 닫기 버튼 클릭 이벤트 핸들러
    closeModal.onclick = function() {
        modal.style.display = 'none';
    }

    // 모달 외부 클릭 시 모달 닫기
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }

    // 이벤트 폼 제출 이벤트 핸들러
    document.getElementById('event-form').addEventListener('submit', function(event) {
        event.preventDefault(); // 폼 기본 동작 방지
        const eventName = document.getElementById('event-name').value;
        const addToChecklist = document.getElementById('add-to-checklist').checked;

        console.log(`Event: ${eventName}, Add to checklist: ${addToChecklist}`);

        // 선택된 슬롯에만 색상 적용
        selectedSlotsIndices.forEach(index => {
            const slot = document.querySelector(`.time-slot[data-index="${index}"]`);
            slot.style.backgroundColor = colors[colorIndex % colors.length]; // 색상을 배열에서 선택
            slot.textContent = eventName.charAt(index - selectedSlotsIndices[0]); // 슬롯에 한 글자씩 넣기
        });

        // 다음 색상 선택
        colorIndex++;

        // 체크박스가 선택된 경우에만 할 일 목록에 추가
        if (addToChecklist) {
            addToChecklistUI(eventName);
        }

        modal.style.display = 'none';
        clearSelection();
    });

// 할 일 목록에 항목을 추가하는 함수
function addToChecklistUI(taskName) {
    // 이미 존재하지 않는 경우에만 추가
    if (!checkIfTaskExists(taskName)) {
        // 새로운 리스트 아이템 생성
        const listItem = document.createElement('li');
        // 리스트 아이템 내용 설정
        listItem.innerHTML = `<div class="task-item"><input type="checkbox"> <span>${taskName}</span><div class="buttons" style="display: none;"><button class="delete">Delete</button><button class="edit">Edit</button></div></div>`;
        // 할 일 목록에 추가
        todoList.appendChild(listItem);

        // 리스트 아이템 클릭 시 버튼 토글
        const taskItem = listItem.querySelector('.task-item');
        taskItem.addEventListener('click', function(event) {
            const target = event.target;
            // 클릭된 요소가 체크박스가 아닌 경우에만 버튼 토글
            if (!target.matches('input[type="checkbox"]')) {
                const buttons = taskItem.querySelector('.buttons');
                buttons.style.display = buttons.style.display === 'none' ? 'block' : 'none';
            }
        });

        // Delete 버튼 클릭 시 항목 삭제
        listItem.querySelector('.delete').addEventListener('click', function() {
            listItem.remove();
        });
    }
}

    // 할 일 목록에 이미 존재하는지 확인하는 함수
    function checkIfTaskExists(taskName) {
        const tasks = todoList.querySelectorAll('li span');
        for (let task of tasks) {
            if (task.textContent === taskName) {
                return true;
            }
        }
        return false;
    }

    // 선택 해제하는 함수
    function clearSelection() {
        const selectedSlots = document.querySelectorAll('.time-slot.selected');
        selectedSlots.forEach(slot => {
            slot.classList.remove('selected');
        });
        selectedSlotsIndices = [];
    }

    // 범위 선택하는 함수
    function selectRange(start, end) {
        for (let i = Math.min(start, end); i <= Math.max(start, end); i++) {
            const slot = document.querySelector(`.time-slot[data-index="${i}"]`);
            slot.classList.add('selected');
            selectedSlotsIndices.push(i); // 선택된 슬롯의 인덱스를 배열에 추가
        }
    }

    // 마우스 다운 이벤트 핸들러
    function handleMouseDown(event) {
        const index = parseInt(event.target.dataset.index, 10);
        if (selectedSlotsIndices.includes(index)) {
            return; // 이미 선택된 슬롯 클릭 시 아무 동작도 하지 않음
        }
        isDragging = true;
        startSlot = index;
        lastSelectedSlot = event.target;
        event.target.classList.add('selected');
    }

    // 마우스 오버 이벤트 핸들러
    function handleMouseOver(event) {
        if (isDragging) {
            endSlot = parseInt(event.target.dataset.index, 10);
            clearSelection();
            selectRange(startSlot, endSlot);
            if (lastSelectedSlot) {
                const lastSlotIndex = parseInt(lastSelectedSlot.dataset.index, 10);
                const currentIndex = parseInt(event.target.dataset.index);
                const minIndex = Math.min(lastSlotIndex, currentIndex);
                const maxIndex = Math.max(lastSlotIndex, currentIndex);
                for (let i = minIndex; i <= maxIndex; i++) {
                    const slot = document.querySelector(`.time-slot[data-index="${i}"]`);
                    slot.classList.add('selected');
                }
            }
            lastSelectedSlot = event.target;
        }
    }

    // 마우스 업 이벤트 핸들러
    function handleMouseUp(event) {
        if (!isDragging) {
            return; // 드래그 상태가 아닌 경우 아무 동작도 하지 않음
        }
        isDragging = false;
        modal.style.display = 'block';

        const startTimeIndex = Math.min(startSlot, endSlot);
        const endTimeIndex = Math.max(startSlot, endSlot);

        selectRange(startTimeIndex, endTimeIndex);

        const startTime = convertIndexToTime(startTimeIndex);
        const endTime = convertIndexToTime(endTimeIndex + 1);

        document.getElementById('start-time').value = startTime;
        document.getElementById('end-time').value = endTime;

        startSlot = startTimeIndex;
        endSlot = endTimeIndex;

        // 선택된 슬롯의 인덱스를 배열에 저장
        selectedSlotsIndices = [];
        for (let i = startSlot; i <= endSlot; i++) {
            selectedSlotsIndices.push(i);
        }
        // 드래그 종료 후, 추가 이벤트 리스너 삭제
        document.removeEventListener('mousemove', handleMouseOver);
        // lastSelectedSlot 변수 업데이트
         lastSelectedSlot = document.querySelector(`.time-slot[data-index="${endSlot}"]`);

    }

    // 마우스 우클릭 이벤트 핸들러
    function handleContextMenu(event) {
        event.preventDefault(); // 기본 우클릭 동작 방지

        const slotIndex = parseInt(event.target.dataset.index, 10);
        if (selectedSlotsIndices.includes(slotIndex)) {
            const contextMenu = document.createElement('div');
            contextMenu.classList.add('context-menu');

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', function() {
                selectedSlotsIndices.forEach(index => {
                    const slot = document.querySelector(`.time-slot[data-index="${index}"]`);
                    slot.style.backgroundColor = ''; // 슬롯 배경 색상 초기화
                    slot.textContent = ''; // 슬롯 텍스트 초기화
                    slot.classList.remove('selected'); // 선택된 상태 해제
                });
                selectedSlotsIndices = []; // 선택된 슬롯 인덱스 초기화
                contextMenu.remove(); // 컨텍스트 메뉴 삭제
            });

            const editButton = document.createElement('button');
            editButton.textContent = 'Edit';
            editButton.addEventListener('click', function() {
                modal.style.display = 'block';
                const startTimeIndex = Math.min(...selectedSlotsIndices);
                const endTimeIndex = Math.max(...selectedSlotsIndices);

                const startTime = convertIndexToTime(startTimeIndex);
                const endTime = convertIndexToTime(endTimeIndex + 1);

                document.getElementById('start-time').value = startTime;
                document.getElementById('end-time').value = endTime;
                contextMenu.remove(); // 컨텍스트 메뉴 삭제
            });

            contextMenu.appendChild(deleteButton);
            contextMenu.appendChild(editButton);
            document.body.appendChild(contextMenu);

            contextMenu.style.top = `${event.clientY}px`;
            contextMenu.style.left = `${event.clientX}px`;

            // 컨텍스트 메뉴 외부 클릭 시 메뉴 삭제
            window.addEventListener('click', function onClickOutsideContext(event) {
                if (!contextMenu.contains(event.target)) {
                    contextMenu.remove();
                    window.removeEventListener('click', onClickOutsideContext);
                }
            });
        }
    }
    // ESC 키를 눌렀을 때 드래그 초기화
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            clearSelection();
        }
    });
});
