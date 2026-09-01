$(document).ready(function () {
    // 1. Smooth page entry
    $(".container").fadeIn(300);

    const $realPasswordModal = $(".real_password");
    const $targetContainer = $realPasswordModal.find("> div");

    // 2. Combined Reveal Handler for both buttons and links
    $(document).on("click", ".reveal_password_click, .reveal_password_button", function (e) {
        e.preventDefault();
        
        // Use currentTarget to ensure we read data-target from the bound element even if an inner icon is clicked
        const passwordValue = $(this).attr("data-target") || "";

        // Inject structured content with a quick Copy button
        $targetContainer.html(`
            <div class="text-center py-3 w-100">
                <small class="text-white-50 text-uppercase fw-bold d-block mb-2" style="letter-spacing: 1px;">
                    Decrypted Secret
                </small>
                <div class="p-3 bg-dark bg-opacity-50 rounded-3 border border-light border-opacity-25 mb-3">
                    <code id="revealedSecretText" class="text-white fs-5 fw-bold user-select-all text-break">
                        ${passwordValue}
                    </code>
                </div>
                <button type="button" class="btn btn-sm btn-light fw-semibold shadow-sm copy-revealed-btn">
                    📋 Copy to Clipboard
                </button>
            </div>
        `);

        // Show overlay with flex display
        $realPasswordModal.css("display", "flex").hide().fadeIn(250);
    });

    // 3. Close Modal Handler
    $(".close_button").click(function () {
        $realPasswordModal.fadeOut(200);
    });

    // 4. One-Click Copy Handler
    $(document).on("click", ".copy-revealed-btn", function () {
        const secret = $("#revealedSecretText").text().trim();
        const $btn = $(this);

        if (navigator.clipboard && secret) {
            navigator.clipboard.writeText(secret).then(() => {
                $btn.html("✅ Copied!").addClass("btn-success text-white").removeClass("btn-light");
                setTimeout(() => {
                    $btn.html("📋 Copy to Clipboard").addClass("btn-light").removeClass("btn-success text-white");
                }, 2000);
            });
        }
    });

    // 5. Close on Escape key press
    $(document).keyup(function (e) {
        if (e.key === "Escape" && $realPasswordModal.is(":visible")) {
            $realPasswordModal.fadeOut(200);
        }
    });
});