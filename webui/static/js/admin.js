$(document).ready(function() {
    $('#loadUsers').click(function(e) {
        e.preventDefault();
        loadSection('users');
    });

    $('#loadTicketTemplates').click(function(e) {
        e.preventDefault();
        loadSection('ticket_templates', displayTicketTemplates);
    });

    $('#loadElementTemplates').click(function(e) {
        e.preventDefault();
        loadSection('element_templates', displayElementTemplates);
    });

    function loadSection(section, displayFunction) {
        $.ajax({
            url: `/api/admin/${section}`,
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    displayFunction(data.items);
                } else {
                    alert(data.message);
                }
            },
            error: function() {
                $('#content').html('<p>Error loading the data.</p>');
            }
        });
    }

    function displayTicketTemplates(items) {
        var content = '<h2>Ticket Templates</h2>';
        items.forEach(item => {
            content += `<div><strong>ID:</strong> ${item.template_id}, <strong>Name:</strong> ${item.name}, <strong>Initial State:</strong> ${item.initial_state}</div>`;
            content += '<ul>';
            for (const [action, transitions] of Object.entries(item.state_transitions)) {
                content += `<li>${action}: ${transitions.map(t => t.description || t.action).join(', ')}</li>`;
            }
            content += '</ul>';
        });
        $('#content').html(content);
    }

    function displayElementTemplates(items) {
        var content = '<h2>Element Templates</h2>';
        items.forEach(item => {
            content += `<div><strong>ID:</strong> ${item.template_id}, <strong>Name:</strong> ${item.name}, <strong>Category:</strong> ${item.category}</div>`;
            if (item.component_templates.length) {
                content += '<ul>';
                item.component_templates.forEach(ct => {
                    content += `<li>Component ID: ${ct.element_template_id}, Quantity: ${ct.quantity}</li>`;
                });
                content += '</ul>';
            } else {
                content += '<p>No components defined.</p>';
            }
        });
        $('#content').html(content);
    }
});
