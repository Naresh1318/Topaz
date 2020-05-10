<template>
  <div>
    <v-layout align-center>
      <v-card style="margin: auto; padding: 2rem" :max-width="card_width()">
        <v-container grid-list-md>
          <v-layout justify-center wrap>
            <v-flex xl3>
              <h1>Topaz</h1>
            </v-flex>
            <v-flex xl10>
              <v-text-field v-model="username" label="Name" required color="dark"></v-text-field>
            </v-flex>
            <v-flex xl10>
              <v-text-field v-model="password" type="password" label="Password"
                            required color="dark"></v-text-field>
            </v-flex>
            <v-flex xl3>
              <v-btn @click="login()" color="dark" dark>Login</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
  </v-layout>
  <v-snackbar v-model="show_alert">
      Wrong username or password <v-btn color="#fff" text @click="show_alert=false">Close</v-btn>
  </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: 'Login',
      show_alert: false,
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      this.$http.post(`${this.$backend_address}/login`, {
        username: this.username,
        password: this.password,
      },
      {
        withCredentials: true,
      })
        .then((response) => {
          if (!response.data.logged_in) {
            this.username = '';
            this.password = '';
            this.show_alert = true;
          } else {
            window.location.href = '/admin';
          }
        });
    },
    is_mobile() {
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return true;
      }
      return false;
    },
    card_width() {
      if (this.is_mobile()) {
        return '90%';
      }
      return '40%';
    },
  },
};
</script>

<style scoped>

</style>
