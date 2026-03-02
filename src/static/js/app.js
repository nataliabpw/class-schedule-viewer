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
        document.getElementById('schedule-container').innerHTML = '<p>Ładowanie...</p>';

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

        const title = document.createElement('h2');
        title.textContent = data.schedule_name;
        scheduleDiv.appendChild(title);

        const subtitle = document.createElement('h3');
        subtitle.textContent = `${data.selected_date} - ${data.weekday}`;
        scheduleDiv.appendChild(subtitle);

        if (data.schedule.length === 0) {
            const noClasses = document.createElement('p');
            noClasses.textContent = 'Brak zajęć w tym dniu.';
            scheduleDiv.appendChild(noClasses);
            return;
        }

        // Table
        const table = document.createElement('table');
        const headerRow = document.createElement('tr');
        ['Start', 'Koniec', 'Zajęcia', 'Dodatkowe informacje'].forEach(text => {
            const th = document.createElement('th');
            th.textContent = text;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        data.schedule.forEach(entry => {
            const row = document.createElement('tr');
            [entry.start, entry.end, entry.name, entry.info].forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                row.appendChild(td);
            })
            table.appendChild(row);
        })
        scheduleDiv.appendChild(table);
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