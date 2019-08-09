let vue_login = new Vue({
    el: "#app",
    vuetify: new Vuetify(),
    data: {
        show_alert: false,
        username: "",
        password: "",
    },
    methods: {
        /**
         * Try logging in user
         */
        login: function() {
            axios.post("/login", {
                username: vue_login.username,
                password: vue_login.password
            })
                .then(function(response) {
                    if (!response["data"]["logged_in"]) {
                        vue_login.username = ""
                        vue_login.password = ""
                        vue_login.show_alert = true
                    }
                    else {
                        window.location.href = "/admin";
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