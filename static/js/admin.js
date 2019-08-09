let vue_admin = new Vue({
    el: "#app",
    vuetify: new Vuetify(),
    data: {
        types: ["blog", "publication"],
        title: "",
        description: "",
        url: "",
        image_url: "",
        time_stamp: "",
        type: "",
        show_alert: false,
        alert_text: ""
    },
    methods: {
        /**
         * Try submitting entry
         */
        submit_entry: function() {
            if (vue_admin.type === "") {
                this.alert_text = "Fill all entries"
                this.show_alert = true
            }
            axios.post(`/${vue_admin.type}s`, {
                "title": vue_admin.title,
                "description": vue_admin.description,
                "url": vue_admin.url,
                "image_url": vue_admin.image_url,
                "time_stamp": vue_admin.time_stamp
            })
                .then(function(response) {
                    if (response.data["INFO"]) {
                        vue_admin.alert_text = response.data["INFO"]
                        vue_admin.show_alert = true
                    }
                })
        },
        is_mobile: function() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true
            }
            else {
                return false
            }
        },
        card_width: function() {
            if (this.is_mobile())
                return "90%"
            else
                return "40%"
        },
    }
})