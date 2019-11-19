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

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
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

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
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
        const apiURL = "http://127.0.0.1:8000/trusted_institutions_list";

        const $localization = $('#localization').find("div.dropdown").find("div").text();
        const $organization_search = $("#organization_search").val();
        const $help = [];
        $.each($("input[name^='help']:checked"), function () {
            $help.push($(this).data("id"));
        });

        console.log($help);
        console.log($organization_search);
        console.log($localization);

        const data = {
            'localization': $localization,
            'institution_name': $organization_search,
            'target_groups[]': $help,
            // 'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        };


        function loadTrustedInstitutions() {
            $.ajax({
                url: apiURL,
                method: "GET",
                data: data,
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

        $trustedInstitutions.empty();
        loadTrustedInstitutions();


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
     * Summary before form submit
     */
    $("#summary").on("click", function () {
        const $gift_types = [];
        $.each($("input[name='gift_type']:checked"), function () {
            $gift_types.push($(this).parent().find("span.description").text());
        });
        const $bags_number = $("input[name='number_of_bags']").val();
        const $summary_gift_types = `Worki: ${$bags_number}; Oddajesz: ${$gift_types.join(", ")}`;
        $("#summary_gift_types").text($summary_gift_types);

        const $trusted_institution = $("input[name='trusted_institution']:checked").parent().find("div.title").text();
        $("#summary_trusted_institution").text($trusted_institution);

        const $summary_address = $("#summary_address");
        const $li_street = $("<li>").text(`${$("input[name='street']").val()}`);
        const $li_city = $("<li>").text(`${$("input[name='city']").val()}`);
        const $li_postal_code = $("<li>").text(`${$("input[name='postal_code']").val()}`);
        const $li_phone_number = $("<li>").text(`${$("input[name='phone_number']").val()}`);
        $summary_address.empty();
        $summary_address.append($li_street, $li_city, $li_postal_code, $li_phone_number);

        const $summary_date_and_time = $("#summary_date_and_time");
        const $li_date = $("<li>").text(`${$("input[name='pick_up_date']").val()}`);
        const $li_time = $("<li>").text(`${$("input[name='pick_up_time']").val()}`);
        const $notes = $("textarea[name='comments']").val();
        if ($notes === "") {
            var $li_notes = $("<li>").text("Brak uwag");
        } else {
            var $li_notes = $("<li>").text($notes);
        }
        $summary_date_and_time.empty();
        $summary_date_and_time.append($li_date, $li_time, $li_notes);
    })
});
