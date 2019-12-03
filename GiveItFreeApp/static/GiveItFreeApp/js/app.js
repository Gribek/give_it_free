document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        changePage(e) {
            e.preventDefault();
            const $page = e.target;
            const $pageButtonsContainer = $page.parentElement.parentElement;
            const $pageItemsContainers = $pageButtonsContainer.parentElement.querySelectorAll('.help--slides-items');

            [...$pageButtonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $page.classList.add("active");

            const $currentPage = $page.dataset.page;

            $pageItemsContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.page === $currentPage) {
                    el.classList.add("active");
                }
            });
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;


            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;
        }

        /**
         * Submit form
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});


$(function () {

    /**
     * Trusted institutions search in form
     */
    $("#institution_search_button").on("click", function () {
        const $trustedInstitutions = $(".trusted_institutions");
        const $help = [];
        $.each($("input[name^='help']:checked"), function () {
            $help.push($(this).data("id"));
        });

        const $data = {
            'localization': $('#localization').find("div.dropdown div").text(),
            'institution_name': $("#organization_search").val(),
            'target_groups[]': $help,
        };

        $trustedInstitutions.empty();
        loadTrustedInstitutions();

        console.log($data);

        function loadTrustedInstitutions() {
            $.ajax({
                url: "http://127.0.0.1:8000/trusted_institutions_list",
                method: "GET",
                data: $data,
                dataType: "json"
            }).done(function (resp) {
                if (resp.length === 0) {
                    const $div = $("<h3>").text("Brak fundacji pasujących do wprowadzonych danych");
                    $div.appendTo($trustedInstitutions);
                } else {
                    resp.forEach(trustedInstitution => {
                        insertTrustedInstitution(trustedInstitution);
                    });
                }
            }).fail(function (xhr, status, err) {
                console.log(xhr, status, err);
            });
        }


        function insertTrustedInstitution(trustedInstitution) {
            const $div = $("<div class='form-group form-group--checkbox'>");
            const $label = $("<label>");
            const $input = $("<input type='radio' name='trusted_institution'>").attr("value", trustedInstitution.id);
            const $span = $("<span class='checkbox radio'>");
            const $spanDescription = $("<span class='description'>");
            const $divTitle = $("<div class='title'>").text(trustedInstitution.name);
            const $divSubtitle = $("<div class='subtitle'>").text(trustedInstitution.purpose);

            $spanDescription.append($divTitle, $divSubtitle);
            $label.append($input, $span, $spanDescription);
            $div.append($label);
            $div.appendTo($trustedInstitutions);
        }

    });

    let $errors = [];

    /**
     * Save data to database
     */
    $("#gift_form_submit").on("click", function () {
        const apiURL = "http://127.0.0.1:8000/gift_form_submit";
        const $data = ($('#gift_form')).serializeArray();
        console.log($data);

        $.ajax({
            url: `${apiURL}`,
            method: "POST",
            data: $data,
            dataType: "json"
        }).done(function (resp) {
            console.log(resp)
        }).fail(function (xhr, status, err) {
            console.log(xhr, status, err);
        });
    });

    /**
     * Summary before form submit & form validation
     */
    $("#summary").on("click", function () {
        $errors = [];

        const $gift_types = [];
        $.each($("input[name='gift_type']:checked"), function () {
            $gift_types.push($(this).parent().find("span.description").text());
        });
        if ($gift_types.length === 0) {
            $errors.push("rodzaj daru")
        }
        const $bags_number = $("input[name='number_of_bags']").val();
        const $summary_gift_types = `Worki: ${$bags_number}; Oddajesz: ${$gift_types.join(", ")}`;
        $("#summary_gift_types").text($summary_gift_types);
        if ($bags_number === "") {
            $errors.push("ilość worków")
        }

        const $trusted_institution = $("input[name='trusted_institution']:checked").parent().find("div.title").text();
        $("#summary_trusted_institution").text($trusted_institution);
        if ($trusted_institution === "") {
            $errors.push("organizacja")
        }

        const $summary_address = $("#summary_address");
        const $street = `${$("input[name='street']").val()}`;
        const $city = (`${$("input[name='city']").val()}`);
        const $postal_code = (`${$("input[name='postal_code']").val()}`);
        const $phone_number = (`${$("input[name='phone_number']").val()}`);
        $summary_address.empty();
        $summary_address.append($("<li>").text($street), $("<li>").text($city),
            $("<li>").text($postal_code), $("<li>").text($phone_number));
        if ($street === "" || $city === "" || $postal_code === "" || $phone_number === "") {
            $errors.push("adres odbioru")
        }

        const $summary_date_and_time = $("#summary_date_and_time");
        const $date = (`${$("input[name='pick_up_date']").val()}`);
        const $time = (`${$("input[name='pick_up_time']").val()}`);
        const $notes = $("textarea[name='comments']").val();
        const $li_notes = $("<li>");
        if ($notes === "") {
            $li_notes.text("Brak uwag");
        } else {
            $li_notes.text($notes);
        }
        $summary_date_and_time.empty();
        $summary_date_and_time.append($("<li>").text($date), $("<li>").text($time), $li_notes);
        if ($date === "" || $time === "") {
            $errors.push("data odbioru")
        }
        if ($errors.length !== 0) {
            $("#gift_form_submit").hide();
            $("div.errors").text(`Uzupełnij następujące informacje: ${$errors.join(", ")}`);
        } else {
            $("#gift_form_submit").show();
            $("div.errors").text("")
        }
    })
});
