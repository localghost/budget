function parseIo($row) {
    var name = $('td[name="description"] input', $row).val();
    var amount = parseFloat($('td[name="amount"]', $row).text().replace(',', '.'));
    var category = $('td[name="category"] select', $row).find(':selected').text();
    var date = $('td[name="date"]', $row).text();

    var io = {
        'name': name,
        'amount': amount,
        'registered': date + 'T00:00'
    }
    if (category != '---') {
        io['category'] = category
    }

    return io
}

function importSucceeded() {
    alert("Dane zaimportowane");
    window.location.replace('/registry/');
}

function importFailed() {
    alert("Zaznaczonych danych nie udało się zaimportować.");
}

function importResolved() {
    $('#check-all').prop('checked', false);
}

function importIos() {
    var requests = [];
    var successes = 0, failures = 0;
    $('#io_list tbody tr').each(function() {
        if ($('input:checkbox', this).is(':checked')) {
            var io = parseIo(this);

            var row = this;
            requests.push(
                $.post('/api/io-simple/', io)
                    .done(function() { successes++; $('input:checkbox', row).prop('checked', false); })
                    .fail(function() { failures++; })
            );
        }
    })

    $.when.apply($, requests).done(importSucceeded).fail(importFailed).always(importResolved);
}

$(document).ready(function() {
    $('#check-all').click(function() {
        $('#io_list tbody td input:checkbox').prop('checked', $(this).is(':checked'));
    });
    $('#button-import').click(importIos);
    $.ajaxSetup({
        headers: { "X-CSRFToken": $.cookie("csrftoken") }
    });
})