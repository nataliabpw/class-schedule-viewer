(() => {
    const groupSeminariaSelect = document.getElementById('group-seminaria');
    const groupCwiczeniaSelect = document.getElementById('group-cwiczenia');
    const groupZajeciaSelect = document.getElementById('group-zajecia');
    const form = document.getElementById('schedule-form');
    const errorDiv = document.getElementById('error-container');
    const scheduleDiv = document.getElementById('schedule-container');

    async function fetchSchedule(){
        const button = form.querySelector('button[type="submit"]');

        button.disabled = true;
        document.getElementById('schedule-container').innerHTML = `
            <div class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            </div>
        `;

        const params = new URLSearchParams(new FormData(form)).toString();
        try{
            const response = await fetch(`/api/schedule?${params}`);
            const data = await response.json();
            if (!response.ok) {
                showErrors(data.error || 'Błąd serwera');
                return;
            }
            renderScheduleInPage(data);
        } catch (error) {
            showErrors('Błąd sieci');
        } finally {
        button.disabled = false;
    }
    }

    function showErrors(message) {
        scheduleDiv.innerHTML = '';

        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    function clearErrors(){
        errorDiv.textContent = '';
        errorDiv.style.display = 'none';
    }

    function renderScheduleInPage(data){
        clearErrors();
        scheduleDiv.innerHTML = '';

        const card = document.createElement('div');
        card.classList.add('card', 'shadow-sm', 'mb-4');
        scheduleDiv.appendChild(card);

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');
        card.appendChild(cardBody);

        // Header
        const header = document.createElement('div');
        header.classList.add('mb-3');

        header.innerHTML = `
            <div class="text-center">
                <h5 class="mb-1 fw-semibold">${data.schedule_name}</h5>
                <div class="text-muted small">
                    ${data.selected_date} • ${data.weekday}
                </div>
            </div>
        `;

        cardBody.appendChild(header);

        if (data.schedule.length === 0) {
            const noClasses = document.createElement('p');
            noClasses.classList.add('text-muted');
            noClasses.textContent = 'Brak zajęć w tym dniu.';
            cardBody.appendChild(noClasses);
            return;
        }

        // Table
        const table = document.createElement('table');
        table.classList.add('table', 'table-hover', 'align-middle', 'mt-3', 'text-center');
        
        const thead = document.createElement('thead');
        thead.classList.add('table-light');

        const headerRow = document.createElement('tr');
        ['Start', 'Koniec', 'Zajęcia', 'Dodatkowe informacje'].forEach(text => {
            const th = document.createElement('th');
            th.classList.add('align-middle', 'text-center', 'fw-semibold');
            th.textContent = text;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');

        data.schedule.forEach(entry => {
            const row = document.createElement('tr');
            [entry.start, entry.end, entry.name, entry.info].forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                row.appendChild(td);
            })
            tbody.appendChild(row);
        })
        table.appendChild(tbody);
        cardBody.appendChild(table);
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        fetchSchedule();
    });

    groupSeminariaSelect.addEventListener('change', function() {
        const selectedGroup = this.value;
        
        groupCwiczeniaSelect.innerHTML = "";
        groupZajeciaSelect.innerHTML = "";

        if (!selectedGroup) {
            groupCwiczeniaSelect.innerHTML = '<option value="">-- wybierz najpierw grupę seminaryjną--</option>';
            groupZajeciaSelect.innerHTML = '<option value="">-- wybierz najpierw grupę seminaryjną--</option>';
            return;
        }

        const lettersCwiczenia = ["a", "b"];
        const lettersZajecia = ["a", "b", "c"];

        lettersCwiczenia.forEach( letter => {
            const option = document.createElement('option');
            option.value = selectedGroup + letter;
            option.textContent = selectedGroup + letter;

            groupCwiczeniaSelect.appendChild(option);
        })

        lettersZajecia.forEach( letter => {
            const option = document.createElement('option');
            option.value = selectedGroup + letter;
            option.textContent = selectedGroup + letter;

            groupZajeciaSelect.appendChild(option);
        })
    });

    if (groupSeminariaSelect.value) {
        groupSeminariaSelect.dispatchEvent(new Event('change'));
    }
})();