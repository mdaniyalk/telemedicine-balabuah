$(document).ready(function() {
    // Simulate the bot's initial message
    const initialMessage = "Halo. Apa yang bisa saya bantu?";
    const date = new Date();
    const hour = date.getHours();
    const minute = date.getMinutes();
    const str_time = (hour < 10 ? "0" + hour : hour) + ":" + (minute < 10 ? "0" + minute : minute);
    const botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="static/telemedicine-kkn-icon.webp" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + initialMessage + '<span class="msg_time">' + str_time + '</span></div></div>';
    $("#messageFormeight").append($.parseHTML(botHtml));
});

$(document).ready(function() {
    // Initialize session ID variable
    var sessionId = null;

    // Function to start session and get session ID
    function startSession() {
        $("#text").prop("disabled", true); // Disable input field
        $("#text").prop("required", false); // Disable input field
        $("#send").prop("disabled", true); // Disable send button
        $("#text").attr("placeholder", "Mohon menunggu!"); // Set placeholder text

        $.ajax({
            type: "GET",
            url: "/start-session",
            success: function(response) {
                sessionId = response.sessionId;
                console.log(sessionId);
                $("#text").prop("disabled", false); // Enable input field
                $("#send").prop("disabled", false); // Enable send button
                $("#text").prop("required", true); // Disable input field
                $("#text").attr("placeholder", "Ketikkan pesan anda..."); // Set placeholder text
            },
            error: function(xhr, status, error) {
                console.error("Error starting session:", error);
                $("#text").attr("placeholder", "Terjadi error, silahkan reload halaman ini!"); // Set placeholder text
            }
        });
    }

    // Call startSession function when the document is ready
    startSession();

    // Function to simulate typing animation
    function typeMessage(element, message, interval) {
        let index = 0;
        const length = message.length;
        const typingInterval = setInterval(function() {
            if (index < length-10) {
                const x = Math.floor(Math.random() * 10); // Random value for x
                $(element).html(message.substring(0, index + x));
                index += x;
            } else if (index < length) {
                const x = 1; // Random value for x
                $(element).html(message.substring(0, index + x));
                index += x;
            } else {
                clearInterval(typingInterval);
            }
        }, interval);
    }

    $("#messageArea").on("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Lock the messageArea
        $("#text").prop("disabled", true); // Disable input field
        $("#text").prop("required", false); // Disable input field
        $("#send").prop("disabled", true); // Disable send button
        $("#text").attr("placeholder", "Menunggu jawaban. Mohon menunggu!"); // Set placeholder text
        
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = (hour < 10 ? "0" + hour : hour) + ":" + (minute < 10 ? "0" + minute : minute);
        var rawText = $("#text").val();

        var userHtml =
            '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' +
            rawText +
            '<span class="msg_time_send">' +
            str_time +
            "</span></div><div class='img_cont_msg'><img src='https://upload.wikimedia.org/wikipedia/commons/5/59/User-avatar.svg' class='rounded-circle user_img_msg'></div></div>";

        $("#text").val("");
        $("#messageFormeight").append(userHtml);

        var botHtml =
            '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="static/telemedicine-kkn-icon.webp" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' +
            'Loading<span class="loading-dots"></span>' +
            '<span class="msg_time">' +
            str_time +
            "</span></div></div>";

        var $appendedElement = $($.parseHTML(botHtml));
        $("#messageFormeight").append($appendedElement);

        var loadingDots = $appendedElement.find(".loading-dots");

        var dots = 0;
        var loadingInterval = setInterval(function() {
            loadingDots.text(" .".repeat(dots));
            dots = (dots % 3) + 1; // Cycle through 1, 2, 3 dots
        }, 500);

        // Make AJAX request to /get with session ID
        $.ajax({
            data: {
                msg: rawText,
                session_id: sessionId // Include session ID in the request
            },
            type: "POST",
            url: "/chat",
        }).done(function(data) {
            clearInterval(loadingInterval);
            $appendedElement.find(".msg_cotainer").html(''); // Clear loading message
            
            // Start typing animation
            typeMessage($appendedElement.find(".msg_cotainer"), data, 1);

            // Unlock the messageArea
            $("#text").prop("disabled", false); // Enable input field
            $("#send").prop("disabled", false); // Enable send button
            $("#text").prop("required", true); // Disable input field
            $("#text").attr("placeholder", "Ketikkan pesan anda..."); // Set placeholder text
        }).fail(function(xhr, status, error) {
            console.error("Error getting response:", error);
            
            // Unlock the messageArea in case of failure
            $("#text").prop("disabled", false); // Enable input field
            $("#send").prop("disabled", false); // Enable send button
            $("#text").prop("required", true); // Disable input field
            $("#text").attr("placeholder", "Ketikkan pesan anda..."); // Set placeholder text
        });

        event.preventDefault();
    });
});
