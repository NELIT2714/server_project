$(document).ready(function() {
    $("#features-table").on("click", ".edit-feature-btn", function() {
        const $row = $(this).closest("tr");
        const featureId = $row.data("feature-id");

        $.ajax({
            url: "/admin/get_feature_data/" + featureId,
            method: "POST",
            success: function(data) {
                $row.find(".feature-name").html('<input type="text" class="edit-name" value="' + data.name + '">');
                $row.find(".feature-description").html('<input type="text" class="edit-description" value="' + data.description + '">');

                $row.find(".edit-feature-btn").hide();
                $row.find(".save-feature-btn").show();
            },
            error: function(err) {
                console.log('Error: ', err);
            }
        });
    });

    $('#features-table').on("click", ".save-feature-btn", function() {
        const $row = $(this).closest('tr');
        const featureId = $row.data("feature-id");
        const newName = $row.find(".edit-name").val();
        const newDescription = $row.find(".edit-description").val();

        $.ajax({
            url: "/admin/update_feature/" + featureId,
            method: "POST",
            data: { name: newName, description: newDescription },
            success: function(response) {
                $row.find(".feature-name").text(newName);
                $row.find(".feature-description").text(newDescription);

                $row.find(".edit-feature-btn").show();
                $row.find(".save-feature-btn").hide();
            },
            error: function(err) {
                console.log("Error: ", err);
            }
        });
    });

    $('#features-table').on("click", ".delete-btn", function() {
        const $row = $(this).closest('tr');
        const featureId = $row.data("feature-id");

        $.ajax({
            url: "/admin/delete/feature/" + featureId,
            method: "POST",
            success: function(response) {
                $(`tr[data-feature-id="${featureId}"]`).remove();
            },
            error: function(err) {
                console.log("Error: ", err);
            }
        });
    });
});

